// ======================================
// STUDENT PERFORMANCE ANALYZER
// FRONTEND - BACKEND CONNECTION & SMART EVALUATOR
// ======================================

const studentForm = document.getElementById("studentForm");
const analyzeButton = document.getElementById("analyzeButton");
const errorMessage = document.getElementById("errorMessage");

function showError(msg) {
    if (!errorMessage) return;
    errorMessage.textContent = msg;
    errorMessage.classList.add("show");
}

function clearError() {
    if (!errorMessage) return;
    errorMessage.textContent = "";
    errorMessage.classList.remove("show");
}

function getFieldValue(id, altId) {
    const el = document.getElementById(id) || (altId ? document.getElementById(altId) : null);
    return el ? el.value : "";
}

// ======================================
// CLIENT-SIDE EVALUATION ENGINE
// Fallback so the app works seamlessly even
// if the local Python server is not started
// ======================================

function evaluateStudentLocally(studentData) {
    const marks = {
        "Python": studentData["Python"],
        "Web Development": studentData["Web Development"],
        "DSA": studentData["DSA"],
        "Calculus": studentData["Calculus"]
    };

    const total = Math.round((marks["Python"] + marks["Web Development"] + marks["DSA"] + marks["Calculus"]) * 100) / 100;
    const maximum = 400;
    const percentage = Math.round((total / maximum) * 10000) / 100;

    let strongest = "Python";
    let weakest = "Python";
    let maxScore = -Infinity;
    let minScore = Infinity;

    for (const [subj, score] of Object.entries(marks)) {
        if (score > maxScore) {
            maxScore = score;
            strongest = subj;
        }
        if (score < minScore) {
            minScore = score;
            weakest = subj;
        }
    }

    let status = "Needs Improvement";
    if (percentage >= 85) {
        status = "Excellent";
    } else if (percentage >= 70) {
        status = "Good";
    } else if (percentage >= 50) {
        status = "Average";
    }

    const habits = [];
    if (studentData.attendance >= 85) {
        habits.push("Excellent attendance.");
    } else {
        habits.push("Try to improve your attendance.");
    }

    if (studentData.study_hours >= 4) {
        habits.push("Good daily study routine.");
    } else {
        habits.push("Increase your daily study time.");
    }

    if (studentData.sleep_hours >= 7) {
        habits.push("Your sleep duration is healthy.");
    } else {
        habits.push("Try to get at least 7 hours of sleep.");
    }

    const recommendations = [];
    for (const [subj, score] of Object.entries(marks)) {
        if (score < 40) {
            recommendations.push(`${subj}: Immediate improvement required.`);
        } else if (score < 60) {
            recommendations.push(`${subj}: Practice more questions.`);
        } else if (score < 75) {
            recommendations.push(`${subj}: Revise regularly to improve.`);
        } else {
            recommendations.push(`${subj}: Great performance. Keep it up!`);
        }
    }

    return {
        name: studentData.name,
        enrollment: studentData.enrollment,
        marks: marks,
        attendance: studentData.attendance,
        study_hours: studentData.study_hours,
        sleep_hours: studentData.sleep_hours,
        performance: {
            total: total,
            maximum: maximum,
            percentage: percentage,
            strongest: strongest,
            weakest: weakest,
            status: status
        },
        habits: habits,
        recommendations: recommendations,
        engine: "standalone"
    };
}

// ======================================
// FORM SUBMISSION
// ======================================

studentForm.addEventListener("submit", async function(event) {
    // Prevent default form submission
    event.preventDefault();
    clearError();

    // Check HTML5 constraints
    if (!studentForm.checkValidity()) {
        studentForm.reportValidity();
        return;
    }

    // Collect and validate string fields
    const name = getFieldValue("name").trim();
    const enrollment = getFieldValue("enrollment").trim();

    if (!name || !enrollment) {
        showError("Please enter both student name and enrollment number.");
        return;
    }

    // Collect numeric values
    const pythonVal = Number(getFieldValue("python", "Python"));
    const webVal = Number(getFieldValue("web_development", "Web Development"));
    const dsaVal = Number(getFieldValue("dsa", "DSA"));
    const calcVal = Number(getFieldValue("calculus", "Calculus"));
    const attendanceVal = Number(getFieldValue("attendance"));
    const studyVal = Number(getFieldValue("study_hours"));
    const sleepVal = Number(getFieldValue("sleep_hours"));

    // Validation checks
    const scores = [
        { name: "Python", val: pythonVal },
        { name: "Web Development", val: webVal },
        { name: "DSA", val: dsaVal },
        { name: "Calculus", val: calcVal }
    ];

    for (const item of scores) {
        if (isNaN(item.val) || item.val < 0 || item.val > 100) {
            showError(`Please enter a valid score between 0 and 100 for ${item.name}.`);
            return;
        }
    }

    if (isNaN(attendanceVal) || attendanceVal < 0 || attendanceVal > 100) {
        showError("Attendance must be between 0% and 100%.");
        return;
    }

    if (isNaN(studyVal) || studyVal < 0 || studyVal > 24) {
        showError("Study hours must be between 0 and 24 hours.");
        return;
    }

    if (isNaN(sleepVal) || sleepVal < 0 || sleepVal > 24) {
        showError("Sleep hours must be between 0 and 24 hours.");
        return;
    }

    const studentData = {
        name: name,
        enrollment: enrollment,
        "Python": pythonVal,
        "Web Development": webVal,
        "DSA": dsaVal,
        "Calculus": calcVal,
        attendance: attendanceVal,
        study_hours: studyVal,
        sleep_hours: sleepVal
    };

    // Set loading state
    analyzeButton.disabled = true;
    analyzeButton.innerHTML = `
        <span>ANALYZING YOUR DATA...</span>
        <span class="button-arrow">⌛</span>
    `;

    try {
        let result = null;

        // Try Python server first
        try {
            const isHttp = window.location.protocol.startsWith("http");
            const endpoint = isHttp ? "/analyze" : "http://localhost:8000/analyze";

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 2000);

            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(studentData),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (response.ok) {
                const data = await response.json();
                if (data.success && data.result) {
                    result = data.result;
                }
            }
        } catch (serverErr) {
            // Python server is not currently running or request was aborted
            console.log("Connecting in standalone mode...");
        }

        // If Python server is offline or unreachable, compute locally
        if (!result) {
            result = evaluateStudentLocally(studentData);
        }

        // Save result in session storage
        sessionStorage.setItem("studentResult", JSON.stringify(result));

        // Update button state while navigating
        analyzeButton.innerHTML = `
            <span>OPENING DASHBOARD...</span>
            <span class="button-arrow">✓</span>
        `;

        // Navigate to result dashboard
        window.location.href = "result.html";

    } catch (error) {
        showError(error.message || "An error occurred while evaluating your data.");

        // Restore button only on error
        analyzeButton.disabled = false;
        analyzeButton.innerHTML = `
            <span>RUN PERFORMANCE ANALYSIS</span>
            <span class="button-arrow">→</span>
        `;
    }
});
