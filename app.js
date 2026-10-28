// app.js — connects the button, the flip card and the question bank.

import { loadRecent, saveRecent, pickQuestion, remember } from "./deck.js";

const FLIP_MS = 600; // keep in sync with --flip-time in style.css

const button = document.getElementById("get-question");
const card = document.getElementById("card");
const faceFront = document.getElementById("face-front");
const faceBack = document.getElementById("face-back");
const message = document.getElementById("message");

let bank = [];
let recent = loadRecent();
let isFlipped = false; // false = front face showing, true = back face showing
let isFlipping = false; // true while the card is mid-flip

async function loadQuestions() {
  const response = await fetch("questions.json");
  if (!response.ok) {
    throw new Error("questions.json not found");
  }
  return response.json();
}

function showNextQuestion() {
  if (isFlipping) return;
  isFlipping = true;

  const next = pickQuestion(bank, recent);
  recent = remember(recent, next.id, bank.length);
  saveRecent(recent);

  // Write the new question on the face that is currently hidden, then flip.
  const hiddenFace = isFlipped ? faceFront : faceBack;
  hiddenFace.textContent = next.question;

  isFlipped = !isFlipped;
  card.classList.toggle("flipped", isFlipped);

  setTimeout(() => { isFlipping = false; }, FLIP_MS);
}

async function start() {
  try {
    bank = await loadQuestions();
    if (bank.length === 0) throw new Error("questions.json is empty");
    button.disabled = false;
    button.addEventListener("click", showNextQuestion);
  } catch (error) {
    message.textContent = "Couldn't load the questions. Check questions.json and reload.";
    console.error(error);
  }
}

start();
