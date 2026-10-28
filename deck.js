// deck.js — decides WHICH question comes next.
//
// The rule: a question can't come back until MORE THAN HALF the bank
// has been shown since it last appeared.
// We do this by remembering the ids of the most recent questions ("recent")
// and never picking from that list.

const STORAGE_KEY = "question-flip-recent-ids";

// How many recent questions are blocked. Example: 20 questions -> 11 blocked.
// We never block the whole bank, so there is always something left to pick.
export function cooldownSize(bankSize) {
  const moreThanHalf = Math.floor(bankSize / 2) + 1;
  return Math.max(0, Math.min(moreThanHalf, bankSize - 1));
}

// Pick a random question that is not in the recent list.
export function pickQuestion(bank, recentIds) {
  const available = bank.filter((q) => !recentIds.includes(q.id));
  const pool = available.length > 0 ? available : bank;
  return pool[Math.floor(Math.random() * pool.length)];
}

// Add the new question to the recent list and drop the oldest ones.
export function remember(recentIds, newId, bankSize) {
  const updated = [...recentIds, newId];
  const keep = cooldownSize(bankSize);
  return updated.slice(updated.length - keep);
}

// Save the recent list so refreshing the page doesn't reset the rule.
export function loadRecent() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

export function saveRecent(recentIds) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(recentIds));
  } catch {
    // Storage can be blocked (private mode). The app still works without it.
  }
}
