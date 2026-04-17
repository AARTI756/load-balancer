window.onload = () => {

    const predictionEl = document.querySelector(".prediction");
    if (!predictionEl) return;

    const circle = document.querySelector(".circle");
    const progress = document.querySelector(".progress-circle");

    if (circle && progress) {
        const value = parseFloat(circle.getAttribute("data-value")) || 0;
        const offset = 440 - (440 * value) / 100;
        progress.style.strokeDashoffset = offset;

        const prediction = predictionEl.innerText.trim();

        if (prediction === "LOW") progress.style.stroke = "#22c55e";
        else if (prediction === "MEDIUM") progress.style.stroke = "#f59e0b";
        else progress.style.stroke = "#ef4444";
    }

    const chartDataEl = document.getElementById("chartData");
    if (chartDataEl && !window.__chartsLoaded) {

        window.__chartsLoaded = true;

        const low = parseFloat(chartDataEl.dataset.low) || 0;
        const med = parseFloat(chartDataEl.dataset.med) || 0;
        const high = parseFloat(chartDataEl.dataset.high) || 0;

        new Chart(document.getElementById("probChart"), {
            type: "bar",
            data: {
                labels: ["LOW", "MEDIUM", "HIGH"],
                datasets: [{
                    label: "Confidence %",
                    data: [low, med, high],
                    backgroundColor: ["#22c55e", "#f59e0b", "#ef4444"]
                }]
            }
        });

        new Chart(document.getElementById("cpuChart"), {
            type: "line",
            data: {
                labels: Array.from({ length: 10 }, (_, i) => i),
                datasets: [{
                    label: "CPU %",
                    data: Array.from({ length: 10 }, () => Math.random() * 100),
                    borderColor: "#38bdf8",
                    fill: true,
                    tension: 0.4
                }]
            }
        });
    }

    // HISTORY SAFE
    const table = document.querySelector("#historyTable tbody");
    if (table) {
        const cpu = document.querySelector("input[name='cpu']")?.value || "-";
        const load = document.querySelector("input[name='load']")?.value || "-";
        const pred = predictionEl.innerText.trim();
        const decision = document.querySelector(".decision-badge")?.innerText || "-";

        const lastRow = table.lastElementChild;
        if (!lastRow || lastRow.children[0].innerText !== cpu) {
            table.innerHTML += `
                <tr>
                    <td>${cpu}</td>
                    <td>${load}</td>
                    <td>${pred}</td>
                    <td>${decision}</td>
                </tr>
            `;
        }
    }

    // INSIGHT
    const insight = document.getElementById("insightBox");
    if (insight) {
        const p = predictionEl.innerText.trim();

        if (p === "HIGH") insight.innerText = "⚠ High load → scale immediately";
        else if (p === "MEDIUM") insight.innerText = "⚡ Medium load → monitor";
        else insight.innerText = "✅ Stable system";
    }

    // TIMELINE SAFE
    const timelineEl = document.getElementById("timelineData");

    if (timelineEl && !window.__timelineLoaded) {
        window.__timelineLoaded = true;

        const hours = JSON.parse(timelineEl.dataset.hours || "[]");
        const preds = JSON.parse(timelineEl.dataset.preds || "[]");
        const decisions = JSON.parse(timelineEl.dataset.decisions || "[]");
        const servers = JSON.parse(timelineEl.dataset.servers || "[]");
        const actions = JSON.parse(timelineEl.dataset.actions || "[]");

        const list = document.getElementById("timeline");
        if (list) {
            list.innerHTML = "";

            hours.forEach((h, i) => {
                setTimeout(() => {
                    const li = document.createElement("li");
                    li.innerHTML = `
                        <b>${h}</b> → ${preds[i]} (${decisions[i]})<br>
                        ⚙ ${actions[i]} → ${servers[i - 1] || 2} → ${servers[i] || 2}
                    `;
                    list.appendChild(li);
                }, i * 300);
            });
        }

        new Chart(document.getElementById("serverChart"), {
            type: "line",
            data: {
                labels: hours,
                datasets: [{
                    label: "Servers",
                    data: servers,
                    borderColor: "#10b981",
                    fill: true
                }]
            }
        });
    }

    const futureEl = document.getElementById("futureData");

    if (futureEl) {
        const hours = JSON.parse(futureEl.dataset.hours || "[]");
        const preds = JSON.parse(futureEl.dataset.preds || "[]");

        const map = { "LOW": 1, "MEDIUM": 2, "HIGH": 3 };
        const numeric = preds.map(p => map[p]);

        new Chart(document.getElementById("futureChart"), {
            type: "line",
            data: {
                labels: hours,
                datasets: [{
                    label: "Future Load",
                    data: numeric,
                    borderColor: "#a78bfa",
                    fill: true,
                    tension: 0.4
                }]
            }
        });
    }    
};