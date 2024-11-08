//Contact button @ home
document.addEventListener("DOMContentLoaded", () => {
    const contactButton = document.getElementById("contactButton");
    const contactForm = document.getElementById('contactForm');

    if (contactButton) {
        contactButton.addEventListener("click", () => {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }
    //Contact Form Button
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();  

            const formData = new FormData(this);

            fetch('http://127.0.0.1:8000/contact/', {  
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);  
                    contactForm.reset();  
                } else {
                    alert("Something went wrong. Please try again.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("There was an issue with your submission.");
            });
        });
    }
});

//Carousel for reviews
const carouselSlides = document.querySelectorAll('.carousel-slide');
let currentIndex = 0;

function showNextSlide() {
    currentIndex = (currentIndex + 1) % carouselSlides.length;
    carouselSlides.forEach((slide, index) => {
        slide.style.transform = `translateX(-${currentIndex * 100}%)`;
    });
}

setInterval(showNextSlide, 3000);

//FAQ Toggle
const faqQuestions = document.querySelectorAll('.faq-question');

faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
        const answer = question.nextElementSibling;
        const isHidden = answer.style.maxHeight === '0px' || answer.style.maxHeight === '';
        if (isHidden) {
            answer.classList.add('show');
            answer.style.maxHeight = answer.scrollHeight + 'px';
        } else {
            answer.classList.remove('show');
            answer.style.maxHeight = '0px';
        }
        question.classList.toggle('bold');
    });
});

//Arrival time window drop down @ booknow
document.addEventListener("DOMContentLoaded", () => {
    const timeDropdown = document.getElementById("time-dropdown");

    function populateTimeOptions() {
        const startHour = 7; // Open Time
        const endHour = 21; // Close Time
        const interval = 60;

        for (let hour = startHour; hour <= endHour; hour++) {
            const option = document.createElement("option");
            const formattedHour = hour > 12 ? hour - 12 : hour; 
            const ampm = hour >= 12 ? "PM" : "AM";
            option.value = `${hour}:00`;
            option.textContent = `${formattedHour}:00 ${ampm}`;
            timeDropdown.appendChild(option);
        }
    }

    populateTimeOptions();
});

document.addEventListener("DOMContentLoaded", () => {
    const totalPriceElement = document.getElementById("price");

    const prices = {
        extras: {
            fridge: 20.00,
            oven: 20.00,
            deepCleaning: 30.00,
            interiorWindows: 20.00,
            walls: 20.00,
            moveInOut: 60.00,
            loadOfLaundry: 20.00,
            insideCabinets: 20.00
        },
        frequency: { one: 0, weekly: 20, biweekly: 15, monthly: 10 }, // % discounts
        bedroom: 50.00,
        bathroom: 30.00
    };

    let totalPrice = 0.00;
    let selectedExtras = [];
    let selectedFrequency = "one"; 

    function updateTotalPrice() {
        const bedroomCount = parseInt(document.getElementById('bedroom-dropdown').value) || 0;
        const bathroomCount = parseInt(document.getElementById('bathroom-dropdown').value) || 0;
        console.log("Bedroom Count:", bedroomCount);
        console.log("Bathroom Count:", bathroomCount);
    
        totalPrice = (bedroomCount * prices.bedroom) + (bathroomCount * prices.bathroom);
        console.log("Base Total Price (bedrooms + bathrooms):", totalPrice);
    
        selectedExtras.forEach(extra => {
            if (prices.extras[extra] !== undefined) {
                totalPrice += prices.extras[extra];
            }
        });
        console.log("Total after Extras:", totalPrice);
    
        if (prices.frequency[selectedFrequency] !== undefined) {
            const discountPercentage = prices.frequency[selectedFrequency];
            totalPrice -= totalPrice * (discountPercentage / 100); // Apply percentage discount
        }
        console.log("Total after Frequency Discount:", totalPrice);
    
        totalPriceElement.innerText = `$${totalPrice.toFixed(2)}`;
    }

    document.getElementById('bedroom-dropdown').addEventListener('change', updateTotalPrice);
    document.getElementById('bathroom-dropdown').addEventListener('change', updateTotalPrice);

    document.querySelectorAll(".extras input[type='checkbox']").forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            const extra = checkbox.value;
            if (checkbox.checked) {
                selectedExtras.push(extra);
            } else {
                selectedExtras = selectedExtras.filter(e => e !== extra);
            }
            updateTotalPrice();
        });
    });

    document.querySelectorAll('button[id$="-button"]').forEach(button => {
        button.addEventListener('click', () => {
            const frequency = button.id.replace('-button', '');
            if (selectedFrequency !== frequency) {
                selectedFrequency = frequency;
                document.querySelectorAll('button[id$="-button"]').forEach(btn => btn.classList.remove('selected'));
                button.classList.add('selected');
                updateTotalPrice();
            }
        });
    });

    // BookNow Submit Button
    const bookingForm = document.getElementById("bookingForm");
    bookingForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(bookingForm);
        const formDataJSON = {};
        formData.forEach((value, key) => formDataJSON[key] = value);

        const selectedBedrooms = formData.get("bedrooms"); 
        const selectedBathrooms = formData.get("bathrooms"); 
        const cleaningDate = formData.get("cleaningDate"); 
        const cleaningTime = formData.get("cleaningTime"); 

        formDataJSON.totalPrice = totalPrice.toFixed(2);
        formDataJSON.selectedBedrooms = selectedBedrooms;
        formDataJSON.selectedBathrooms = selectedBathrooms;
        formDataJSON.cleaningDate = cleaningDate;
        formDataJSON.cleaningTime = cleaningTime;
        formDataJSON.frequency = selectedFrequency;
        formDataJSON.selectedExtras = selectedExtras;

        console.log("Form Data:", formDataJSON);

        try {
            const response = await fetch("http://127.0.0.1:8000/submit/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formDataJSON)
            });

            if (response.ok) {
                console.log("Submission successful.");
            } else {
                alert("There was an error submitting the form. Please try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Submission failed. Please check your connection and try again.");
        }
    });

    updateTotalPrice();
});

