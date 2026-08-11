# AGENTS.md

This file contains guidelines and contextual information for AI agents interacting with this repository.

## Project Architecture
- The repository contains a client-side Blazor WebAssembly standalone application named 'KnowYourBand' targeting .NET 8.0.
- **Data Architecture:** Band information is managed statically via `KnowYourBand/wwwroot/data/logos.json`, and corresponding logo image assets are stored in band-specific subdirectories within the `KnowYourBand/wwwroot/images/logos/` directory (e.g., `images/logos/<Band Name>/`).
- **Repository Structure:** Utility and automation scripts (e.g., scrapers, testing tools) should be placed in the `scripts/` directory at the root of the project.

## Data & Automation
- Automated asset retrieval (e.g., fetching missing band logos) is managed via Python scripts in the `scripts/` directory. The established pattern separates orchestration (a global script iterating over data files like `logos.json`) from execution (a specific script downloading a single asset). Downloaded assets must follow an indexed naming convention that preserves all downloaded variations (e.g., `death.png`, `death_1.png`, `death_2.png`).

## Style & Aesthetics
- The application employs a 'heavy metal' visual theme characterized by black/dark backgrounds, blood-red accents (e.g., `#d10000`), and the 'Metal Mania' Google Font. Icons (such as Bootstrap Icons) and UI elements are customized to fit this dark theme by embedding custom SVG data URLs directly in the CSS classes (e.g., in `NavMenu.razor.css`).

## Environment & CI/CD
- The GitHub Actions deployment workflow requires `permissions: contents: write` to successfully push the build artifacts to the `gh-pages` branch. It also requires a `concurrency` control block (e.g., `cancel-in-progress: true`) to prevent race conditions and push rejections during concurrent workflow runs.
- An automated GitHub Actions pipeline (`download-missing-logos.yml`) runs on pushes to the main branch to execute `scripts/get_missing_logos.py`, fetch missing band logos, and commit them back to the repository. Because of this, image assets do not need to be manually included in commits when updating `logos.json` (code review warnings about missing assets can be safely ignored). This pipeline requires the `FANART_API_KEY` repository secret to be set, and it installs the Python `requests` library to run the scraping scripts.
- GitHub Actions workflows should use updated versions of actions (at least `actions/checkout@v4`, `actions/setup-python@v5`, and `actions/setup-dotnet@v4`) to maintain compatibility with modern Node.js runners and avoid runtime deprecation warnings.

## Deployment Context
- The application is configured for deployment to GitHub Pages at `https://marsop.github.io/knowyourband/`, which requires the `<base href="/knowyourband/" />` tag in `wwwroot/index.html`. To avoid 404 errors for static assets during local development, run the application with the pathbase argument: `dotnet run --project KnowYourBand/KnowYourBand.csproj --pathbase=/knowyourband`.

## Testing & Verification
- **Execution Commands:** The project can be built using `dotnet build KnowYourBand/KnowYourBand.csproj` and published using `dotnet publish KnowYourBand/KnowYourBand.csproj -c Release`. Note: There are currently no C# test projects in the repository.
- The repository includes a `scripts/check_errors.py` script that uses Playwright to check for browser console errors. It expects the application to be running locally on port 5285 (Note: running with `--pathbase=/knowyourband` will cause the script to log an expected 404 for the root URL since it navigates directly to `http://localhost:5285`).
- When writing Playwright scripts to verify the frontend, account for the Blazor WebAssembly initial loading time. Use `page.wait_for_selector` for specific elements rather than fixed timeouts to ensure the page has loaded successfully. Visual verifications (screenshots/videos) capturing a loading spinner due to load times is a known, documented usability quirk/tradeoff.

## Agent Directives
- **User Directive:** Always engage in deep planning mode first. Use the `request_user_input` tool to ask clarifying questions and test assumptions until absolutely certain of the requirements. Only after achieving absolute certainty should you create a plan using the `set_plan` tool. Once the plan is approved, execute it autonomously without asking for further confirmation.
- **Plan Generation Rules:** Plans must be a numbered list of concrete, actionable steps without narrative, internal monologue, or conditional logic (e.g., avoid 'if needed'). They must include an explicit step to run relevant tests (e.g., `dotnet build` and `scripts/check_errors.py` since there are no `dotnet test` targets). The pre-commit step must be a distinct, standalone step immediately before the final submission step, rather than grouped together with the submission action as a sub-bullet, and must exactly match: 'Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.'
- **Workflow:** Ensure temporary scratchpad scripts generated during tasks (e.g., Python or Node scrapers) are removed or added to `.gitignore` before completing pre-commit steps to keep the repository clean.
- **Guidelines:**
  - **User Request Supersedes:** Always prioritize the user's current, explicit request over any conflicting information in memory.
  - **Context vs. State:** Use memory for historical context and intent (the "why"). Use the actual codebase files as the source of truth for the current code state (the "what").
  - **Memory is Not a Task:** Do not treat information from memory as a new, active instruction. Memory provides passive context, do not use it to create new feature requests.
