const jsPsychSortableRank = (function (jspsych) {
  "use strict";

  const info = {
    name: "sortable-rank",
    parameters: {
      items: {
        type: jspsych.ParameterType.ARRAY,
        pretty_name: "Items",
        default: [],
        description: "Array of HTML strings/elements for each item.",
      },
      labels: {
        type: jspsych.ParameterType.ARRAY,
        pretty_name: "Labels",
        default: [],
        description: "Labels corresponding to items (same length as items).",
      },
      instructions: {
        type: jspsych.ParameterType.STRING,
        pretty_name: "Instructions",
        default: "Drag and drop the items to assign them to teams.",
        description: "Trial instructions displayed at the top.",
      },
      animation_duration: {
        type: jspsych.ParameterType.INT,
        pretty_name: "Animation Duration",
        default: 150,
        description: "Animation speed for drag and drop (ms).",
      },
      team_labels: {
        type: jspsych.ParameterType.ARRAY,
        pretty_name: "Team Labels",
        default: ["Team A", "Unsorted Items", "Team B"],
        description: "Labels for the left, middle, and right columns.",
      },
      required_items_team_a: {
        type: jspsych.ParameterType.INT,
        pretty_name: "Required Items in Team A",
        default: null,
        description:
          "How many items must be in Team A before submission is allowed.",
      },
      error_message: {
        type: jspsych.ParameterType.STRING,
        pretty_name: "Error Message",
        default:
          "Please assign the required number of items to Your Team before proceeding.",
        description:
          "Displayed if participant tries to submit without required items in Team A.",
      },
      unsorted_items_error_message: {
        type: jspsych.ParameterType.STRING,
        pretty_name: "Unsorted Items Error Message",
        default: "Please assign all items to a team before proceeding.",
        description:
          "Displayed if participant tries to submit with items left in the unsorted area.",
      },
      lock_first_item_team_a: {
        type: jspsych.ParameterType.BOOL,
        pretty_name: "Lock First Item (Team A)",
        default: true,
        description: "If true, the first item is locked in Team A.",
      },
      lock_second_item_team_b: {
        type: jspsych.ParameterType.BOOL,
        pretty_name: "Lock Second Item (Team B)",
        default: true,
        description: "If true, the second item is locked in Team B.",
      },
      unsorted_grid_columns: {
        type: jspsych.ParameterType.INT,
        pretty_name: "Unsorted Grid Columns",
        default: 2,
        description:
          "Number of columns for the unsorted area (2 means two items side-by-side).",
      },
    },
  };

  class SortableRankPlugin {
    constructor(jsPsych) {
      this.jsPsych = jsPsych;
    }

    trial(displayElement, trial) {
      // Validate items vs labels
      if (trial.labels.length !== trial.items.length) {
        console.error(
          "Length of labels array does not match length of items array.",
        );
        return;
      }
      // Validate team_labels
      if (!Array.isArray(trial.team_labels) || trial.team_labels.length !== 3) {
        console.error(
          "team_labels must be an array of three labels (left, middle, right).",
        );
        return;
      }

      // Clear display
      displayElement.innerHTML = "";

      // Instructions
      if (trial.instructions) {
        const instructionsEl = document.createElement("p");
        instructionsEl.innerHTML = trial.instructions;
        displayElement.appendChild(instructionsEl);
      }

      // Container for columns
      const containerDiv = document.createElement("div");
      containerDiv.className = "sortable-container";

      // Left column (Team A)
      const leftColumn = document.createElement("div");
      leftColumn.className = "sortable-column";
      const leftHeader = document.createElement("h3");
      leftHeader.textContent = trial.team_labels[0];
      const leftList = document.createElement("ul");
      leftList.id = "team-left";
      leftList.className = "sortable-list";
      leftColumn.appendChild(leftHeader);
      leftColumn.appendChild(leftList);

      // Middle column (Unsorted)
      const middleColumn = document.createElement("div");
      middleColumn.className = "sortable-column sortable-middle-column";
      const middleHeader = document.createElement("h3");
      middleHeader.textContent = trial.team_labels[1];
      const middleList = document.createElement("ul");
      middleList.id = "unsorted-items";
      middleList.className = "sortable-list sortable-grid";
      middleColumn.appendChild(middleHeader);
      middleColumn.appendChild(middleList);

      // Right column (Team B)
      const rightColumn = document.createElement("div");
      rightColumn.className = "sortable-column";
      const rightHeader = document.createElement("h3");
      rightHeader.textContent = trial.team_labels[2];
      const rightList = document.createElement("ul");
      rightList.id = "team-right";
      rightList.className = "sortable-list";
      rightColumn.appendChild(rightHeader);
      rightColumn.appendChild(rightList);

      // Append columns
      containerDiv.appendChild(leftColumn);
      containerDiv.appendChild(middleColumn);
      containerDiv.appendChild(rightColumn);
      displayElement.appendChild(containerDiv);

      // Lock the first item in Team A if requested
      if (trial.lock_first_item_team_a && trial.items.length > 0) {
        const lockedItemA = this.createItemElement(0, trial.items[0], true);
        leftList.appendChild(lockedItemA);
      }

      // Lock the second item in Team B if requested
      if (trial.lock_second_item_team_b && trial.items.length > 1) {
        const lockedItemB = this.createItemElement(1, trial.items[1], true);
        rightList.appendChild(lockedItemB);
      }

      // Place the remaining items into the unsorted area
      trial.items.forEach((itemHtml, index) => {
        if (trial.lock_first_item_team_a && index === 0) return;
        if (trial.lock_second_item_team_b && index === 1) return;
        const itemElement = this.createItemElement(index, itemHtml, false);
        middleList.appendChild(itemElement);
      });

      // Insert plugin default CSS if not present
      if (!document.getElementById("sortable-rank-styles")) {
        const style = document.createElement("style");
        style.type = "text/css";
        style.id = "sortable-rank-styles";
        style.innerHTML = `
          /* 3-column grid for container */
          .sortable-container {
            display: grid;
            grid-template-columns: 1fr 1.5fr 1fr;
            gap: 10px;
            width: 100%;
            box-sizing: border-box;
          }

          .sortable-column {
            display: flex;
            flex-direction: column;
          }

          .sortable-list {
            min-height: 200px;
            border: 1px solid #ccc;
            padding: 5px;
            list-style-type: none;
            margin-top: 5px;
          }

          .sortable-grid {
            display: grid;
            grid-row-gap: 10px;
            grid-column-gap: 10px;
          }

          .sortable-item {
            margin: 5px;
            padding: 5px;
            border: 1px solid #aaa;
            background-color: #f9f9f9;
            cursor: move;
            display: flex;
            align-items: center;
          }

          .sortable-item.locked-item {
            background-color: #e0e0e0;
            cursor: default;
          }

          .sortable-item.locked-item .lock-icon {
            margin-right: 5px;
          }

          .rank-number {
            font-weight: bold;
            margin-right: 5px;
          }

          @media (max-width: 900px) {
            .sortable-container {
              grid-template-columns: 1fr 1fr;
            }
          }
        `;
        document.head.appendChild(style);
      }

      // Set grid columns for unsorted area
      const unsortedCols = trial.unsorted_grid_columns || 2;
      middleList.style.gridTemplateColumns = `repeat(${unsortedCols}, 1fr)`;

      // Track the order in which items are FIRST moved out of the unsorted area
      let firstRemovals = []; // array of {itemIndex, time, from, to}
      const movedItems = new Set(); // track which items have already been moved once

      // Update rank numbers in Team A/B
      function updateRankNumbers() {
        let globalRank = 1;
        [leftList, rightList].forEach((list) => {
          const items = list.querySelectorAll(".sortable-item");
          items.forEach((item) => {
            const rankNumberEl = item.querySelector(".rank-number");
            rankNumberEl.textContent = globalRank++;
          });
        });
        // Clear rank numbers for items in unsorted
        middleList
          .querySelectorAll(".sortable-item .rank-number")
          .forEach((el) => {
            el.textContent = "";
          });
      }

      // Initialize Sortable
      setTimeout(() => {
        const sortableOptions = {
          group: {
            name: "shared",
            pull: (to, from, dragEl) => {
              return !dragEl.classList.contains("locked-item");
            },
            put: true,
          },
          animation: trial.animation_duration,

          // onEnd is triggered whenever an item is dropped in a new location
          onEnd: (evt) => {
            updateRankNumbers();

            // If the item was removed from the middle list
            if (evt.from.id === "unsorted-items") {
              const itemIdAttr = evt.item.getAttribute("data-id");
              if (itemIdAttr !== "locked") {
                const itemIndex = parseInt(itemIdAttr, 10);
                // If we haven't recorded this item being removed yet, record now
                if (!movedItems.has(itemIndex)) {
                  movedItems.add(itemIndex);
                  firstRemovals.push({
                    itemIndex: itemIndex,
                    timestamp: performance.now(),
                    from: "unsorted",
                    to: evt.to.id,
                  });
                }
              }
            }
          },
        };

        [leftList, middleList, rightList].forEach((ul) => {
          new Sortable(ul, sortableOptions);
        });
      }, 100);

      // Initial rank
      updateRankNumbers();

      // Submit button
      const endTrialBtn = document.createElement("button");
      endTrialBtn.id = "end-trial-btn";
      endTrialBtn.textContent = "Submit";
      displayElement.appendChild(endTrialBtn);

      endTrialBtn.addEventListener("click", () => {
        const getListData = (ul) => {
          const items = Array.from(ul.querySelectorAll(".sortable-item"));
          return items.map((item) => {
            const idAttr = item.getAttribute("data-id");
            if (idAttr === "locked") {
              return {
                index: "locked",
                label: "locked",
                content: item.innerHTML,
              };
            }
            const idx = parseInt(idAttr, 10);
            return {
              index: idx,
              label: trial.labels[idx],
              content: trial.items[idx],
            };
          });
        };

        const unsortedItems = getListData(middleList);
        const teamLeftItems = getListData(leftList);
        const teamRightItems = getListData(rightList);

        // Validation: No items left unsorted
        if (unsortedItems.length > 0) {
          alert(trial.unsorted_items_error_message);
          return;
        }

        // Validation: required_items_team_a
        if (trial.required_items_team_a !== null) {
          const numItemsInTeamA = teamLeftItems.length;
          if (numItemsInTeamA !== trial.required_items_team_a) {
            alert(trial.error_message);
            return;
          }
        }

        // Prepare the final data object
        const trialData = {
          unsorted_items: unsortedItems,
          team_left_items: teamLeftItems,
          team_right_items: teamRightItems,
          first_removal_order: firstRemovals,
        };

        // End trial
        this.jsPsych.finishTrial(trialData);
      });
    }

    // Helper: create the <li> element for each item
    createItemElement(index, itemHtml, isLocked) {
      const li = document.createElement("li");
      li.className = "sortable-item";
      if (isLocked) {
        li.classList.add("locked-item");
        li.setAttribute("data-id", "locked");
      } else {
        li.setAttribute("data-id", index);
      }

      const rankNumber = document.createElement("span");
      rankNumber.className = "rank-number";
      rankNumber.textContent = "";
      li.appendChild(rankNumber);

      if (isLocked) {
        const lockIcon = document.createElement("span");
        lockIcon.className = "lock-icon";
        lockIcon.textContent = "🔒";
        li.appendChild(lockIcon);
      }

      const contentDiv = document.createElement("div");
      contentDiv.innerHTML = itemHtml;
      li.appendChild(contentDiv);

      return li;
    }
  }

  SortableRankPlugin.info = info;
  return SortableRankPlugin;
})(jsPsychModule);
