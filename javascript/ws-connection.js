(() => {
    const BACKEND_CONSOLE_POLLING_TIMEOUT = 500;


    document.addEventListener('DOMContentLoaded', () => {
        onCodeBlockReady(setupLayout);
    });


    function onCodeBlockReady(callback) {
        const ready = getLinesContainerComponents() !== null;
        if(!ready) {
            setTimeout(() => onCodeBlockReady(callback), BACKEND_CONSOLE_POLLING_TIMEOUT);
            return;
        }
        callback();
    }


    function setupLayout() {
        const overflowComponents = getOverflowComponents();
        overflowComponents.forEach(overflow => { overflow.style.maxHeight = '360px'; });

        const observer = new MutationObserver((mutationsList, observer) => {
            mutationsList.forEach((mutation) => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    const scrollableComponents = getScrollableComponents();
                    scrollableComponents.forEach(scrollable => {
                        if(scrollable.getAttribute('force-scroll-down') === 'true') {
                            scrollable.setAttribute('force-scroll-down', 'false');
                            const scrollMem = [window.scrollX, window.scrollY];
                            scrollable.scrollTop = scrollable.scrollHeight;
                            requestAnimationFrame(() => window.scrollTo(...scrollMem));
                        }
                    });
                }
            });
        });
        const observerConfig = { childList: true };
        getLinesContainerComponents().forEach(container => {
            container.setAttribute('contenteditable', false);
            observer.observe(container, observerConfig);
        });

        const url = document.querySelector('#backend_console_websocket_url').getAttribute('data-url');
        createWebsocket(url);
    }


    function createWebsocket(url) {
        const socket = new WebSocket(`ws://${url}/sd-webui-backend-console`);

        socket.onopen = (event) => {
            console.log('[sd-webui-backend-console] WS - connected');
        };

        socket.onclose = (event) => {
            console.log('[sd-webui-backend-console] WS - disconnected');
        };

        socket.onmessage = (event) => {
            const message = JSON.parse(event.data).message;
            let trimmed = message;
            if(trimmed.startsWith('\n')) trimmed = trimmed.substring(1);
            // TODO: parse ANSI escape codes and replace them with css style
            trimmed = removeEscapeSequences(trimmed);
            if(trimmed.trim() === '') return;

            getScrollableComponents().forEach(scrollable => scrollable.setAttribute('force-scroll-down', 'true'));

            getLinesContainerComponents().forEach(container => {
                const newLine = document.createElement('div');
                newLine.innerHTML = trimmed;
                container.appendChild(newLine);
            });
        };
    }


    function removeEscapeSequences(text) {
        const escapeRegex = /\u001b\[[0-9;]*[a-zA-Z]/g;
        return text.replace(escapeRegex, '');
    }


    function getOverflowComponents() {
        return document.querySelectorAll('div.backend-console-textbox div.wrap div.codemirror-wrapper div.cm-editor');
    }


    function getScrollableComponents() {
        const overflowComponents = getOverflowComponents();
        if(overflowComponents.length === 0) return null;
        return Array.from(overflowComponents).map(c => c.querySelector('div.cm-scroller'));
    }


    function getLinesContainerComponents() {
        const scrollableComponents = getScrollableComponents();
        if(scrollableComponents === null) return null;
        return Array.from(scrollableComponents).map(c => c.querySelector('div.cm-content'));
    }
})();
