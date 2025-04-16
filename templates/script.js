function generateResume() {
    document.getElementById("r-name").innerText = document.getElementById("name").value;
    document.getElementById("r-email").innerText = document.getElementById("email").value;
    document.getElementById("r-phone").innerText = document.getElementById("phone").value;
    document.getElementById("r-linkedin").innerText = document.getElementById("linkedin").value;
    document.getElementById("r-education").innerText = document.getElementById("education").value;
    document.getElementById("r-experience").innerText = document.getElementById("experience").value;
    document.getElementById("r-skills").innerText = document.getElementById("skills").value;
    document.getElementById("r-projects").innerText = document.getElementById("projects").value;
}

function downloadResume() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.text("Resume", 10, 10);
    doc.text(`Name: ${document.getElementById("name").value}`, 10, 20);
    doc.text(`Email: ${document.getElementById("email").value}`, 10, 30);
    doc.text(`Phone: ${document.getElementById("phone").value}`, 10, 40);
    doc.text(`LinkedIn: ${document.getElementById("linkedin").value}`, 10, 50);
    doc.text(`Education: ${document.getElementById("education").value}`, 10, 60);
    doc.text(`Experience: ${document.getElementById("experience").value}`, 10, 80);
    doc.text(`Skills: ${document.getElementById("skills").value}`, 10, 100);
    doc.text(`Projects: ${document.getElementById("projects").value}`, 10, 120);

    doc.save("Resume.pdf");
}

function downloadExcel() {
    let resumeData = [
        ["Full Name", "Email", "Phone", "LinkedIn", "Education", "Experience", "Skills", "Projects"],
        [
            document.getElementById("name").value,
            document.getElementById("email").value,
            document.getElementById("phone").value,
            document.getElementById("linkedin").value,
            document.getElementById("education").value,
            document.getElementById("experience").value,
            document.getElementById("skills").value,
            document.getElementById("projects").value
        ]
    ];

    let wb = XLSX.utils.book_new();
    let ws = XLSX.utils.aoa_to_sheet(resumeData);
    XLSX.utils.book_append_sheet(wb, ws, "Resume Data");

    XLSX.writeFile(wb, "Resume_Data.xlsx");
}
