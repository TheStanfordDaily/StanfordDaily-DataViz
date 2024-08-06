console.log("Medal-tracker js running...");

document.addEventListener('DOMContentLoaded', function() {
    // Inject CSS
    const style = document.createElement('style');
    style.textContent = `
        body {
            font-family: 'Fira Sans', sans-serif;
            font-weight: 300;
            font-size: larger;
            background-color: #f5f5f5;
        }
        .medal-table-container {
            width: 100%;
            max-width: 750px;
            margin: 0 auto;
        }
        .medal-table {
            width: 100%;
            margin: auto;
        }
        .medal-table-header,
        .medal-table-row {
            display: grid;
            grid-template-columns: 1fr 3fr 1fr 1fr 1fr 1fr 1fr;
            align-items: center;
            padding: 10px;
        }
        .medal-table-header {
            font-weight: 400;
        }
        .medal-table-row {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: 300;
        }
        .education-details-container,
        .athlete-details-container {
            display: none;
            padding: 10px;
        }
        .education-details-container {
            margin-top: -15px;
            padding: 0;
            border: 1px solid #ddd;
        }
        .athlete-details-container {
            border-top: 1px solid #ddd;
            border-bottom: 1px solid #ddd;
        }
        .medal-table-sub-row {
            margin: 0;
            border: 0;
            border-radius: 0;
        }
        .medal-count {
            text-align: center;
        }
        .total-medal-icon,
        .expand-collapse {
            width: 20px;
            height: 20px;
            vertical-align: middle;
            cursor: pointer;
        }
        .black-background {
            background-color: black;
            color: white;
        }
        button {
            margin-left: auto;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 25px;
            height: 25px;
            border: 1px solid black;
            border-radius: 25%;
            background-color: white;
            cursor: pointer;
        }
        .gold, .silver, .bronze {
            display: inline-block;
            width: 24px;
            height: 24px;
            line-height: 24px;
            border-radius: 50%;
            text-align: center;
            margin: auto;
            border: 1px solid black;
        }
        .gold {
            background-color: #F4CA72;
        }
        .silver {
            background-color: #E5E5E5;
        }
        .bronze {
            background-color: #D0B189;
        }
        .athlete-details {
            display: flex;
            flex-direction: row;
        }
        .athlete-frame {
            margin-left: 10px;
            margin-right: 10px;
            width: 30%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .athlete-photo {
            width: min(100%, 150px);
            aspect-ratio: 1 / 1;
            object-fit: cover;
            object-position: top;
            border-radius: 5px;
        }
        .athlete-info {
            width: 70%;
        }
        .athlete-info h2 {
            margin: 0;
            font-size: 24px;
            font-weight: bold;
        }
        .athlete-info p {
            margin: 5px 0;
        }
        .athlete-info p strong {
            display: inline-block;
        }
        @media (max-width: 480px) {
            .athlete-photo {
                height: 100%;
            }
        }
    `;
    document.head.appendChild(style);

    // Inject HTML
    const container = document.getElementById('medal-tracker-content');
    container.innerHTML = `
        <div class="medal-table-container">
            <div class="medal-table">
                <div class="medal-table-header">
                    <div>Rank</div>
                    <div>School</div>
                    <div class="medal-count gold">G</div>
                    <div class="medal-count silver">S</div>
                    <div class="medal-count bronze">B</div>
                    <div class="medal-count total"><img src="https://stanforddaily.com/wp-content/uploads/2024/08/medalAll.svg" alt="Total Medals" class="total-medal-icon"></div>
                    <div></div>
                </div>
                <div id="medal-table-rows"></div>
            </div>
        </div>
    `;

    d3.csv("./output.csv").then(function(data) {
        const educationData = d3.group(data, d => d.education || "None");
        const medalTableRows = d3.select("#medal-table-rows");

        // Calculate totals for each education group and store them in an array
        const educationTotalsArray = [];
        educationData.forEach((athletes, education) => {
            const educationKey = education.replace(/[^a-zA-Z0-9]/g, '_');
            const educationTotals = athletes.reduce((totals, athlete) => {
                totals.gold += +athlete.medals_gold;
                totals.silver += +athlete.medals_silver;
                totals.bronze += +athlete.medals_bronze;
                return totals;
            }, { gold: 0, silver: 0, bronze: 0 });

            educationTotals.total = educationTotals.gold + educationTotals.silver + educationTotals.bronze;
            educationTotalsArray.push({ education, educationKey, totals: educationTotals, athletes });
        });

        // Sort the array by total medals
        educationTotalsArray.sort((a, b) => b.totals.total - a.totals.total);

        // Create rows for each education group
        educationTotalsArray.forEach((educationData, index) => {
            const { education, educationKey, totals, athletes } = educationData;

            // Sort athletes within each education group by total medals
            athletes.sort((a, b) => 
                (+b.medals_gold + +b.medals_silver + +b.medals_bronze) - 
                (+a.medals_gold + +a.medals_silver + +a.medals_bronze)
            );

            // Assign educationKey and athleteIndex to each athlete for easier matching
            athletes.forEach((athlete, athleteIndex) => {
                athlete.educationKey = educationKey;
                athlete.athleteIndex = athleteIndex;
            });

            // Append a row for each education group
            const row = medalTableRows.append("div").attr("class", "medal-table-row");

            row.html(`
                <div class="medal-order">${index + 1}</div>
                <div>${education}</div>
                <div class="medal-count">${totals.gold}</div>
                <div class="medal-count">${totals.silver}</div>
                <div class="medal-count">${totals.bronze}</div>
                <div class="medal-count">${totals.total}</div>
                <button onclick="toggleEducationDetails('${educationKey}')">
                    <img src="./assets/expand.svg" alt="Expand" class="expand-collapse">
                </button>
            `);

            // Append a container for each education group's details
            medalTableRows.append("div")
                .attr("class", "education-details-container")
                .attr("id", `education-details-${educationKey}`);

            // Append a row for each athlete within the education group
            athletes.forEach((athlete, athleteIndex) => {
                const athleteRow = d3.select(`#education-details-${educationKey}`).append("div")
                    .attr("class", "medal-table-row medal-table-sub-row");

                athleteRow.html(`
                    <div class="medal-order">${athleteIndex + 1}</div>
                    <div>${athlete.first_name} ${athlete.last_name}</div>
                    <div class="medal-count">${athlete.medals_gold}</div>
                    <div class="medal-count">${athlete.medals_silver}</div>
                    <div class="medal-count">${athlete.medals_bronze}</div>
                    <div class="medal-count">${+athlete.medals_gold + +athlete.medals_silver + +athlete.medals_bronze}</div>
                    <button onclick="toggleAthleteDetails('${educationKey}', ${athleteIndex})">
                        <img src="./assets/expand.svg" alt="Expand" class="expand-collapse">
                    </button>
                `);

                // Append a container for each athlete's details
                d3.select(`#education-details-${educationKey}`).append("div")
                    .attr("class", "athlete-details-container")
                    .attr("id", `athlete-details-${educationKey}-${athleteIndex}`);
            });
        });

        // Store athlete data globally
        window.athleteData = data;
    });
});

/**
 * Toggles the visibility of education group details.
 * @param {string} educationKey - The unique key identifying the education group.
 */
function toggleEducationDetails(educationKey) {
    const detailsDiv = document.getElementById(`education-details-${educationKey}`);
    const isVisible = detailsDiv.style.display === "block";
    detailsDiv.style.display = isVisible ? "none" : "block";
    updateToggleButton(detailsDiv.previousElementSibling.querySelector('button'), isVisible);
}

/**
 * Toggles the visibility of athlete details.
 * @param {string} educationKey - The unique key identifying the education group.
 * @param {number} index - The index of the athlete within the education group.
 */
function toggleAthleteDetails(educationKey, index) {
    const detailsDiv = document.getElementById(`athlete-details-${educationKey}-${index}`);
    const isVisible = detailsDiv.style.display === "block";
    detailsDiv.style.display = isVisible ? "none" : "block";
    updateToggleButton(detailsDiv.previousElementSibling.querySelector('button'), isVisible);
    if (!isVisible) loadAthleteData(educationKey, index, detailsDiv);
}

/**
 * Updates the expand/collapse button icon and background color.
 * @param {HTMLButtonElement} button - The button element to update.
 * @param {boolean} isVisible - Whether the details are currently visible.
 */
function updateToggleButton(button, isVisible) {
    button.innerHTML = `<img src="${isVisible ? 'https://stanforddaily.com/wp-content/uploads/2024/08/expand.svg' : 'https://stanforddaily.com/wp-content/uploads/2024/08/collapse.svg'}" alt="${isVisible ? 'Expand' : 'Collapse'}" class="expand-icon">`;
    button.classList.toggle('black-background', !isVisible);
}

/**
 * Loads and displays athlete data within the details container.
 * @param {string} educationKey - The unique key identifying the education group.
 * @param {number} index - The index of the athlete within the education group.
 * @param {HTMLElement} container - The container to populate with athlete data.
 */
function loadAthleteData(educationKey, index, container) {
    const athlete = window.athleteData.find(a => a.educationKey === educationKey && a.athleteIndex === index);
    container.innerHTML = `
        <div class="athlete-details">
            <div class="athlete-frame">
                <img src="${athlete.thumbnail_url}" alt="${athlete.thumbnail_alt_text}" class="athlete-photo">
            </div>
            <div class="athlete-info">
                <h2>${athlete.first_name} ${athlete.last_name}</h2>
                <hr>
                <p><strong>Height:</strong> ${athlete.height}</p>
                <p><strong>Age:</strong> ${athlete.age}</p>
                <p><strong>Home:</strong> ${athlete.hometown_city}, ${athlete.hometown_state}</p>
                <p><strong>Sport:</strong> ${athlete.sport}</p>
            </div>
        </div>
    `;
}