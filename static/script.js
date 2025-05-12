const signInBtn = document.getElementById('signInButton');
const signUpBtn = document.getElementById('signUpButton');
const shortenerBtn = document.getElementById('shortenerButton');

function validateAuthFields(emailInput, passwordInput) {
    if (emailInput.includes(" ") || passwordInput.includes(" ")) {
        alert("Can't include ' ' charter");
        return false;
    }

    if (emailInput.length < 5 || passwordInput.length < 5) {
        alert("Length must be more than 5");
        return false;
    }
    return true;
}


if (signInBtn) {
    signInBtn.addEventListener('click', function () {
        const emailInput = document.getElementById("email");
        const passwordInput = document.getElementById("password");

        if (!validateAuthFields(emailInput.value, passwordInput.value)) return;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                user_name: emailInput.value,
                password: passwordInput.value
            })
        })
            .then(async response => {
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || "Sign in failed");
                }
                return response.json();
            })
            .then(data => {
                alert('Success!');
            })
            .catch(error => {
                console.error('Error:', error.message);
                alert('Error: ' + error.message);
            });

    });
}

if (signUpBtn) {
    signUpBtn.addEventListener('click', function () {
        const emailInput = document.getElementById("email");
        const passwordInput = document.getElementById("password");

        if (!validateAuthFields(emailInput.value, passwordInput.value)) return;

        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            },
            credentials: 'include',
            body: JSON.stringify({
                user_name: emailInput.value,
                password: passwordInput.value
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    alert('Registration success');
                }
            })
            .catch(error => {
                console.error('Error during the request:', error);
                alert('Something wrong...');
            });
    });
}

if (shortenerBtn) {
    shortenerBtn.addEventListener('click', function () {
        const longURL = document.getElementById("longURL");

        if (longURL.value.includes(" ")) {
            alert("Can't include ' ' charter");
            return;
        }

        if (longURL.value.length < 5) {
            alert("url length must be more than 5");
            return;
        }


        fetch('/saveUrl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            },
            credentials: 'include',
            body: JSON.stringify({url: longURL.value})
        })
            .then(async response => {
                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.error || 'Unknown error');
                }
                return response.json();
            })
            .then(data => {
                const shortUrl = `${window.location.origin}/${data.short_url}`;
                const resultDiv = document.getElementById("shortResult");
                resultDiv.innerHTML = `✅ Short URL: <a href="${shortUrl}" target="_blank">${shortUrl}</a>`;
            })
            .catch(error => {
                console.error('Ошибка:', error.message);
                alert('❌ Ошибка: ' + error.message);
            });
    });
}
