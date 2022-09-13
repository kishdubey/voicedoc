function deleteWord(wordID) {
  element = document.getElementById(wordID);
  element.innerHTML = `<del>${element.text}</del>`;
  element.style.color = "red";
  element.className = "unvalidWords";
  element.onclick = function () {
    unDeleteWord(wordID);
  };
}

function unDeleteWord(wordID) {
  element = document.getElementById(wordID);
  element.innerHTML = `${element.text}`;
  element.style.color = "#6c757d";
  element.className = "validWords";
  element.onclick = function () {
    deleteWord(wordID);
  };
}

function addWord(wordID) {
  element = document.getElementById(wordID);
  element.innerHTML = " " + prompt("What text would you like to add?") + " ";
  element.style.color = "green";
  element.className = "validWords";
  element.onclick = function () {
    deleteWord(wordID);
  };
}

function getValidWords() {
  var validWords = [];
  elements = document.getElementsByClassName("validWords");
  for (var key in elements) {
    validWords.push(String(elements[key].text).trim());
  }
  return validWords;
}

function getUnvalidWords() {
  var unvalidWords = [];
  elements = document.getElementsByClassName("unvalidWords");
  for (var key in elements) {
    unvalidWords.push(String(elements[key].text).trim());
  }
  return unvalidWords;
}

function setWords() {
  var validWords = getValidWords();
  var unvalidWords = getUnvalidWords();

  document.editForm.validWords.value = validWords;
  document.editForm.unvalidWords.value = unvalidWords;

  return true;
}
