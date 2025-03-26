unction generateResume() {
    document.getElementById("r-name").innerText = document.getElementById("name").value;
    document.getElementById("r-email").innerText = document.getElementById("email").value;
    document.getElementById("r-phone").innerText = document.getElementById("phone").value;
    document.getElementById("r-education").innerText = document.getElementById("education").value;
    document.getElementById("r-experience").innerText = document.getElementById("experience").value;
    document.getElementById("r-skills").innerText = document.getElementById("skills").value;
}

function downloadResume() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    doc.setFont("helvetica");

    let resumeContent = `
        Name: ${document.getElementById("name").value}
        Email: ${document.getElementById("email").value}
        Phone: ${document.getElementById("phone").value}

        Education:
        ${document.getElementById("education").value}

        Experience:
        ${document.getElementById("experience").value}

        Skills:
        ${document.getElementById("skills").value}
    `;

    doc.text(resumeContent, 10, 10);
    doc.save("resume.pdf");
}

