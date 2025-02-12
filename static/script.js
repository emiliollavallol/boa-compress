const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("upload");
const selectFileBtn = document.getElementById("select-file");
const resultsContainer = document.getElementById("results-container");
const processingText = document.getElementById("processing-text");
const downloadAllLink = document.getElementById("download-all");
let selectedFiles = [];
let allBlobs = [];  // ✅ Store optimized files for bulk download

// Click to open file selector
selectFileBtn.addEventListener("click", () => fileInput.click());

// Handle file selection
fileInput.addEventListener("change", function () {
    selectedFiles = Array.from(this.files);
    showFileNames(selectedFiles);
});

// Drag-and-drop events
["dragenter", "dragover"].forEach(eventName => {
    dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        dropArea.classList.add("highlight");
    });
});

["dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        dropArea.classList.remove("highlight");
    });
});

dropArea.addEventListener("drop", function (e) {
    e.preventDefault();
    selectedFiles = Array.from(e.dataTransfer.files);
    showFileNames(selectedFiles);
});

// Display selected file names
function showFileNames(files) {
    dropArea.innerHTML = `<p>${files.length} archivos seleccionados</p>`;
}

// Handle optimization
document.getElementById("convert").addEventListener("click", async function () {
    if (!selectedFiles.length) {
        alert("Selecciona o arrastra imágenes.");
        return;
    }

    resultsContainer.style.display = "block";
    processingText.style.display = "block";
    allBlobs = [];  // ✅ Reset storage for new conversions

    for (const file of selectedFiles) {
        const resultItem = document.createElement("div");
        resultItem.classList.add("progress-item");
        resultItem.innerHTML = `
            <div class="file-info">
                <p>${file.name} (${(file.size / 1024).toFixed(2)} KB)</p>
                <div class="progress-bar"><span></span></div>
                <p class="percentage">Subiendo...</p>
            </div>
            <button class="download-btn">Descargar</button>
        `;

        resultsContainer.appendChild(resultItem);

        const progressBar = resultItem.querySelector(".progress-bar span");
        const percentageText = resultItem.querySelector(".percentage");
        const downloadBtn = resultItem.querySelector(".download-btn");

        const formData = new FormData();
        formData.append("image", file);

        try {
            const response = await fetch("/convert", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Error al procesar ${file.name}`);
            }

            const blob = await response.blob();
            allBlobs.push({ name: file.name, blob });  // ✅ Store for bulk download
            const url = URL.createObjectURL(blob);

            const originalSize = file.size / 1024;
            const optimizedSize = blob.size / 1024;
            const reduction = ((originalSize - optimizedSize) / originalSize * 100).toFixed(2);

            progressBar.style.width = "100%";
            percentageText.innerText = `Reducido ${reduction}% (${optimizedSize.toFixed(2)} KB)`;

            downloadBtn.style.display = "inline-block";
            downloadBtn.onclick = () => {
                const a = document.createElement("a");
                a.href = url;
                a.download = `optimized-${file.name.replace(/\.[^/.]+$/, ".webp")}`; // ✅ Ensure .webp extension
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            };

        } catch (error) {
            percentageText.innerText = "Error al procesar";
        }
    }

    processingText.style.display = "none";
    downloadAllLink.style.display = "inline-block";  // ✅ Show Download All button
});

// ✅ Fix for "Download All" Button
downloadAllLink.addEventListener("click", async function () {
    if (allBlobs.length === 0) {
        alert("No hay imágenes optimizadas para descargar.");
        return;
    }

    const zip = new JSZip();

    allBlobs.forEach((file, index) => {
        zip.file(`optimized_${index + 1}.webp`, file.blob);  // ✅ Ensure .webp extension
    });

    const content = await zip.generateAsync({ type: "blob" });
    const zipLink = document.createElement("a");
    zipLink.href = URL.createObjectURL(content);
    zipLink.download = "compressed_images.zip";
    zipLink.click();
});
