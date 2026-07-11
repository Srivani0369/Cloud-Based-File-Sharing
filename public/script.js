const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const fileContainer = document.getElementById("fileContainer");

uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const res = await fetch("/upload", { method: "POST", body: formData });
  const data = await res.json();
  alert(data.message);
  fileInput.value = "";
  loadFiles();
});

async function loadFiles() {
  const res = await fetch("/files");
  const files = await res.json();
  fileContainer.innerHTML = "";

  files.forEach((file) => {
    const card = document.createElement("div");
    card.className = "file-card";
    card.innerHTML = `
      <a href="/uploads/${file}" target="_blank">${file}</a>
      <div class="actions">
        <button onclick="copyLink('${file}')">🔗</button>
        <button onclick="deleteFile('${file}')">🗑️</button>
      </div>
    `;
    fileContainer.appendChild(card);
  });
}

async function deleteFile(filename) {
  if (confirm(`Delete ${filename}?`)) {
    await fetch(`/delete/${filename}`, { method: "DELETE" });
    loadFiles();
  }
}

function copyLink(filename) {
  const link = `${window.location.origin}/uploads/${filename}`;
  navigator.clipboard.writeText(link);
  alert("Copied link: " + link);
}

loadFiles();
