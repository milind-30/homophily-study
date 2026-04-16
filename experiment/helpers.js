function sampleCharacterImage() {
  const demographics = Object.keys(characterImages);
  const shuffled = jsPsych.randomization.shuffle(demographics);

  for (let i = 0; i < shuffled.length; i++) {
    const key = shuffled[i];
    if (!selectedDemographics.has(key) && !selectedCharacters.has(key)) {
      selectedDemographics.add(key);
      selectedCharacters.add(key);
      const imageList = characterImages[key];
      return imageList[Math.floor(Math.random() * imageList.length)];
    }
  }
  console.warn("No unique characters left to sample.");
  return null;
}

function capitalizeEachWord(string) {
  return string
    .replace(/-/g, " ")
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ")
    .replace(" Or ", "/");
}

function generateCharacterHTML(imagePath) {
  const pathParts = imagePath.split("/");
  const demographicFolder = pathParts[pathParts.length - 2];
  const filename = pathParts[pathParts.length - 1];
  const filenameParts = filename.split("_");
  const ageParts = filenameParts[4].split(".");

  const demographicParts = demographicFolder.split("_");
  const age = ageParts[0];
  const sex = demographicParts[2];
  const race = demographicParts[3];

  return `
      <img src="${imagePath}" alt="Character ${race} ${sex}">
      <div>
        <p>Race: ${capitalizeEachWord(race)}</p>
        <p>Sex: ${capitalizeEachWord(sex)}</p>
        <p>Age: ${age}</p>
      </div>
    `;
}

function generateParticipantHTML(imagePath) {
  return `
      <img src="${imagePath}" alt="Participant">
      <div>
        <p><strong>You (Leader)</strong></p>
      </div>
    `;
}

function generateOpponentHTML(imagePath) {
  return `
      <img src="${imagePath}" alt="Opponent">
      <div>
        <p><strong>Other Team's Leader</strong></p>
      </div>
    `;
}

/**
 * Convert participant or character "raw" inputs into canonical { race, gender, ageBracket }.
 * This single function unifies logic for both participant and character folder parsing.
 *
 * @param {string} rawRace    - Race label or folder segment (e.g. "Asian", "White", "Black", etc.).
 * @param {string} rawGender  - Gender label or folder segment (e.g. "man", "woman", "non-binary").
 * @param {string|number} rawAge - If participant, might be numeric age (21), if character folder, might be "18-24".
 * @returns {Object} { race: string, gender: string, ageBracket: string }
 */
function parseDemographics(rawRace, rawGender, rawAge) {
  // Convert the race to a canonical label
  const raceMap = {
    "south asian": "South Asian",
    "south-asian": "South Asian",
    "east/southeast asian": "East/Southeast Asian",
    "east-asian": "East/Southeast Asian",
    black: "Black",
    white: "White",
    "hispanic/latine/latinx": "Latino",
    latino: "Latino",
    indigenous: "Indigenous",
    multiracial: "Multiracial",
    other: "Other",
  };
  let raceKey = (rawRace || "").toLowerCase().trim();
  const race = raceMap[raceKey] || "Other";

  // Convert gender
  const genderMap = {
    man: "man",
    male: "man",
    woman: "woman",
    female: "woman",
    "non-binary": "non-binary",
    other: "other",
  };
  let genderKey = (rawGender || "").toLowerCase().trim();
  const gender = genderMap[genderKey] || "other";

  // Convert age or bracket
  let ageBracket = "unknown";
  if (typeof rawAge === "number") {
    // participant numeric age
    if (rawAge <= 24) ageBracket = "18-24";
    else if (rawAge >= 25 && rawAge <= 31) ageBracket = "25-31";
    else if (rawAge >= 32 && rawAge <= 38) ageBracket = "32-38";
    else if (rawAge >= 39 && rawAge <= 45) ageBracket = "39-45";
    else if (rawAge > 45) ageBracket = "45+";
  } else {
    // character folder age bracket, e.g. "25-31"
    if (rawAge == '24') ageBracket = '18-24';
    else if (rawAge == '39') ageBracket = '39-45';
    else ageBracket = String(rawAge).trim();
  }
  return { race, gender, ageBracket };
}

/**
 * Counts how many features (race, gender, ageBracket) match between participant & character.
 * @param {Object} demoA - { race, gender, ageBracket }
 * @param {Object} demoB - { race, gender, ageBracket }
 * @returns {number} integer 0..3
 */
function countSharedFeatures(demoA, demoB) {
  let shared = 0;
  if (demoA.race === demoB.race) shared++;
  if (demoA.gender === demoB.gender) shared++;
  if (demoA.ageBracket === demoB.ageBracket) shared++;
  return shared;
}

/**
 * createBuckets()
 * 
 * Returns a structure:
 * {
 *   0: { folderKey1: [imgPaths...], folderKey2: [...], ... },
 *   1: { ... },
 *   2: { ... },
 *   3: { ... }
 * }
 */
function createBuckets(participantDemo, characterImages) {
  const bucketMap = { 0: {}, 1: {}, 2: {}, 3: {} };

  for (const folderKey of Object.keys(characterImages)) {
    const imageList = characterImages[folderKey];
    if (!Array.isArray(imageList)) continue;

    const parts = folderKey.split("_"); 
    if (parts.length < 4) continue;

    const rawAge    = parts[1];
    const rawGender = parts[2];
    const rawRace   = parts[3];

    const charDemo = parseDemographics(rawRace, rawGender, rawAge);
    const shared   = countSharedFeatures(participantDemo, charDemo);
    if (shared < 0 || shared > 3) continue;

    if (!bucketMap[shared][folderKey]) {
      bucketMap[shared][folderKey] = [];
    }
    bucketMap[shared][folderKey].push(...imageList);
  }

  return bucketMap;
}



/**
 * drawBalancedSet(bucketMap, totalNeeded=8)
 * 
 * @param {Object} bucketMap  - {0:{folderKey:[imgPaths]},1:{...},2:{...},3:{...}}
 * @param {number} totalNeeded - total images (8,12, etc.). We'll pick totalNeeded/4 from each bucket.
 * 
 * Logic:
 * - For sharedCount=3: picking multiple images from the same folder is allowed outright (to fill the sampleSize).
 * - For sharedCount=0,1,2: try to pick from distinct folders first. If not enough unique folders, fallback to duplicates in the same folder.
 * 
 * - If we still end up with < totalNeeded, do leftover fallback across all buckets.
 */
function drawBalancedSet(bucketMap, totalNeeded=8) {
  const sampleSize = Math.floor(totalNeeded / 4); 
  let finalResult = [];

  for (let sharedCount = 0; sharedCount < 4; sharedCount++) {
    let needed = sampleSize;
    const folderDict = bucketMap[sharedCount]; // e.g. {folderKey: [imgPaths]}
    const folderKeys = jsPsych.randomization.shuffle(Object.keys(folderDict));

    let picks = [];
    if (sharedCount === 3) {
      // ALLOW multiple picks from the same folder if needed
      for (let f = 0; f < folderKeys.length && needed > 0; f++) {
        const key = folderKeys[f];
        const images = jsPsych.randomization.shuffle(folderDict[key]);
        const pickCount = Math.min(images.length, needed);
        picks.push(...images.slice(0, pickCount));
        needed -= pickCount;
      }
    } else {
      // For buckets 0,1,2: prefer distinct folder usage 
      // => pick only 1 image per folder if possible
      for (let f = 0; f < folderKeys.length && needed > 0; f++) {
        const key = folderKeys[f];
        const images = jsPsych.randomization.shuffle(folderDict[key]);
        if (images.length > 0) {
          picks.push(images[0]); // pick 1 from this folder
          needed--;
        }
      }

      // If we still need more after using distinct folders, fallback to duplicates
      if (needed > 0 && folderKeys.length > 0) {
        // We still need 'needed' more items from bucket sharedCount
        // so let's pick duplicates from the available folders
        // e.g. picking multiple images from the same folder now
        for (let f = 0; f < folderKeys.length && needed > 0; f++) {
          const key = folderKeys[f];
          const images = jsPsych.randomization.shuffle(folderDict[key]);
          
          // We already used 1 image from this folder, so skip that one
          // picks might contain the first image from earlier
          // Let's do leftover = images excluding the one we used (if we used from this folder)
          const leftover = images.filter(img => !picks.includes(img));

          while (leftover.length > 0 && needed > 0) {
            picks.push(leftover.shift());
            needed--;
          }

          if (needed <= 0) break;
        }
      }
    }

    finalResult.push(...picks);
  }

  // Fallback if finalResult < totalNeeded
  if (finalResult.length < totalNeeded) {
    console.warn(`Short bucket sampling. Found ${finalResult.length}, fallback logic...`);
    const leftoverNeeded = totalNeeded - finalResult.length;
    if (leftoverNeeded > 0) {
      let leftoverPool = [];
      for (let s = 3; s >= 0; s--) {
        const fDict = bucketMap[s];
        for (const fKey of Object.keys(fDict)) {
          const leftover = fDict[fKey].filter(img => !finalResult.includes(img));
          leftoverPool.push(...leftover);
        }
      }
      leftoverPool = jsPsych.randomization.shuffle(leftoverPool);
      finalResult.push(...leftoverPool.slice(0, leftoverNeeded));
    }
  }

  if (finalResult.length < totalNeeded) {
    console.warn(`Could only sample ${finalResult.length} images. Partial set returned.`);
  }

  return jsPsych.randomization.shuffle(finalResult).slice(0, totalNeeded);
}




/**
 * Draws TWO distinct sets of 8 images each, with no overlap.
 * Each set is balanced for shared features.
 *
 * Strategy:
 * 1. Build the full bucket map for participant.
 * 2. Draw one set of 8 from the buckets.
 * 3. Remove those 8 from the bucket map.
 * 4. Draw the second set from the updated buckets.
 *
 * @param {Object} participantDemo - participant {race, gender, ageBracket}
 * @param {Object} characterImages - dictionary from character_images.js
 * @returns {Object} {setA: [...], setB: [...]} each is an array of up to 8 distinct images
 */
function drawTwoDistinctSets(participantDemo, characterImages) {
  const bucketMap = createBuckets(participantDemo, characterImages);

  // draw the first set
  const setA = drawBalancedSet(bucketMap, 8);

  // remove setA from the bucketMap
  for (let s = 0; s < 4; s++) {
    for (const folderKey in bucketMap[s]) {
      bucketMap[s][folderKey] = bucketMap[s][folderKey].filter(img => !setA.includes(img));
    }
  }

  // draw second set
  const setB = drawBalancedSet(bucketMap, 8);

  return { setA, setB };
}


/**
 * Generate all pairs for forced choice (i < j).
 */
function generateAllPairs(length) {
  const pairs = [];
  for (let i = 0; i < length; i++) {
    for (let j = i + 1; j < length; j++) {
      pairs.push([i, j]);
    }
  }
  return pairs;
}

/**
 * Rearrange trials to avoid repeating the same character consecutively.
 */
function rearrangeTrials(pairs) {
  const rearranged = [];
  let lastUsed = [];

  while (pairs.length > 0) {
    let found = false;
    for (let i = 0; i < pairs.length; i++) {
      const [a, b] = pairs[i];
      if (!lastUsed.includes(a) && !lastUsed.includes(b)) {
        rearranged.push([a, b]);
        pairs.splice(i, 1);
        lastUsed = [a, b];
        found = true;
        break;
      }
    }
    if (!found) {
      pairs = jsPsych.randomization.shuffle(pairs);
      const pair = pairs.shift();
      rearranged.push(pair);
      lastUsed = [pair[0], pair[1]];
    }
  }
  return rearranged;
}

function parseImageDemographicsFromPath(imagePath) {
  const pathParts = imagePath.split("/");
  // The second-last folder might be "Age_25-31_woman_white"
  // e.g. pathParts[pathParts.length - 2]
  const demoKey = pathParts[pathParts.length - 2]; // e.g. "Age_25-31_woman_white"
  const parts = demoKey.split("_"); // ["Age", "25-31", "woman", "white"]
  if (parts.length < 4) {
    return { race: "Other", gender: "other", ageBracket: "unknown" };
  }
  const rawAge = parts[1]; // e.g. "25-31"
  const rawGender = parts[2]; // e.g. "woman"
  const rawRace = parts[3]; // e.g. "white"

  // This calls the same parseDemographics(...) from helpers.js
  return parseDemographics(rawRace, rawGender, rawAge);
}
