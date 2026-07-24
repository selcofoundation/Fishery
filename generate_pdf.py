import os
from playwright.sync_api import sync_playwright

html_path = os.path.abspath("index.html")
pdf_path = os.path.abspath("India_Fisheries_Handbook_Complete.pdf")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 900})
    page.goto("file:///" + html_path.replace("\\", "/"), wait_until="networkidle", timeout=120000)
    page.wait_for_timeout(5000)

    # Hide sidebar, show main content full width for PDF
    page.evaluate("""() => {
        const sidebar = document.getElementById("sidebar");
        if (sidebar) sidebar.style.display = "none";
        const main = document.querySelector(".main-content") || document.querySelector("#content") || document.querySelector("main");
        if (main) {
            main.style.marginLeft = "0";
            main.style.width = "100%";
            main.style.maxWidth = "100%";
            main.style.padding = "40px";
        }
        const menuBtn = document.getElementById("mobileMenuBtn");
        if (menuBtn) menuBtn.style.display = "none";
        const btt = document.getElementById("backToTop");
        if (btt) btt.style.display = "none";
        document.querySelectorAll(".stat-card, .img-card, .img-card-wide, .species-photo, .chapter-section, .vc-node").forEach(el => {
            el.style.breakInside = "avoid";
        });
    }""")
    page.wait_for_timeout(2000)

    page.pdf(
        path=pdf_path,
        format="A4",
        print_background=True,
        margin={"top": "20mm", "right": "15mm", "bottom": "20mm", "left": "15mm"}
    )
    browser.close()
    print(f"PDF saved: {pdf_path} ({os.path.getsize(pdf_path) / 1024 / 1024:.1f} MB)")
