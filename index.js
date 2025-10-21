// Login Button
document.getElementById("loginBtn").onclick = () => {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  if (!email || !password) {
    alert("Please enter email and password");
  } else {
    // Redirect to welcome page after login
    window.location.href = "welcome.html";
  }
};

// Signup Button
document.getElementById("signupBtn").onclick = () => {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  if (!email || !password) {
    alert("Please enter email and password");
  } else {
    // Redirect to welcome page after signup
    window.location.href = "welcome.html";
  }
};
