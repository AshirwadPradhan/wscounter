window.addEventListener("DOMContentLoaded", () => {
    const ws = new WebSocket("ws://localhost:5678");

    document.querySelector(".minus").addEventListener("click", () => {
        ws.send(JSON.stringify({action: "minus"}));
    });

    document.querySelector(".plus").addEventListener("click", () => {
        ws.send(JSON.stringify({action: "plus"}))
    });

    ws.onmessage = ({data}) => {
        const event = JSON.parse(data);
        switch (event.type) {
            case "value":
                document.querySelector(".value").textContent = event.value;
                break;
            case "users":
                const users = `${event.count} user${event.count == 1 ? "": "s"}`;
                document.querySelector(".users").textContent = users;
                break;
        }
    };
});