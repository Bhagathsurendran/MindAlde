document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ selfcare.js loaded successfully");  // Ensures script is loaded

    let getSuggestionsBtn = document.getElementById("getSuggestionsBtn");
    let categoryDropdown = document.getElementById("category");
    let suggestionsDiv = document.getElementById("suggestions");

    if (getSuggestionsBtn && categoryDropdown && suggestionsDiv) {
        getSuggestionsBtn.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent page reload

            let category = categoryDropdown.value;
            if (!category) {
                alert("⚠️ Please select a category before getting suggestions.");
                return;
            }

            fetch(`/selfcare/get_suggestions?category=${category}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsDiv.innerHTML = ""; // Clear previous results

                    if (data.length === 0) {
                        suggestionsDiv.innerHTML = "<p>No suggestions found for this category.</p>";
                        return;
                    }

                    data.forEach(item => {
                        let suggestionCard = `
                            <div class="suggestion">
                                <h3>${item.name}</h3>
                                <p>${item.description}</p>
                                <button onclick="saveActivity('${item.name}', '${item.type}')">Save</button>
                            </div>
                        `;
                        suggestionsDiv.innerHTML += suggestionCard;
                    });
                })
                .catch(error => console.error("❌ Error fetching suggestions:", error));
        });
    } else {
        console.error("❌ Missing required elements in HTML.");
    }
});

function saveActivity(name, type) {
    if (!name || !type) {
        console.error("❌ Invalid activity data.");
        return;
    }

    fetch("/selfcare/save_activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, type: type })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ Activity saved successfully!");
        } else {
            alert("⚠️ Failed to save activity.");
        }
    })
    .catch(error => console.error("❌ Error saving activity:", error));
}

// function setReminder(activityId, button) {
//     fetch('/set_reminder', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ activity_id: activityId })
//     })
//     .then(response => response.json())
//     .then(data => {
//       if (data.success) {
//         showFlashMessage("✅ Reminder set!", "success");
  
//         // Optionally disable button to avoid duplicates
//         button.disabled = true;
//         button.innerText = "Reminder Set ✅";
  
//         // Reload notifications dynamically
//         loadNotifications();
//       } else {
//         showFlashMessage("❌ Failed to set reminder!", "error");
//       }
//     });
//   }
  
//   function showFlashMessage(message, type) {
//     const flashDiv = document.createElement('div');
//     flashDiv.className = `flash-message ${type}`;
//     flashDiv.innerText = message;
//     document.body.appendChild(flashDiv);
//     setTimeout(() => {
//       flashDiv.remove();
//     }, 1000); // 1 second
//   }
  
//   function loadNotifications() {
//     fetch('/get_notifications')
//       .then(res => res.json())
//       .then(data => {
//         const notifContainer = document.getElementById('notifications');
//         notifContainer.innerHTML = "";
//         data.forEach(item => {
//           notifContainer.innerHTML += `
//             <div class="notif-item">
//               🔔 ${item.activity_id} - ${item.status}
//             </div>
//           `;
//         });
//       });
//   }
document.addEventListener("DOMContentLoaded", function () {
    const userId = localStorage.getItem("user_id");  // Or however you get current user ID

    if (userId) {
        loadSavedActivities(userId);
    }
});

function loadSavedActivities(userId) {
    fetch(`/get_activities?user_id=${userId}`)
        .then(res => res.json())
        .then(data => {
            const todoList = document.getElementById("todoList");
            if (!todoList) return;

            todoList.innerHTML = "";

            data.forEach(activity => {
                todoList.innerHTML += `
                    <div class="todo-item">
                        <strong>${activity.title}</strong><br>
                        🕒 ${activity.reminder_time} <br>
                        Status: ${activity.status}
                        <div>
                            <button onclick="markAs('${activity.title}', 'Done', '${userId}')">✅ Done</button>
                            <button onclick="markAs('${activity.title}', 'Missed', '${userId}')">❌ Missed</button>
                        </div>
                    </div>
                    <hr/>
                `;
            });
        });
}

function markAs(title, status, userId) {
    fetch("/update_activity_status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, title: title, status: status })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || "Status updated");
        loadSavedActivities(userId);  // Refresh the list
    });
}
