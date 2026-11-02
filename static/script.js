const form = document.getElementById("predictionForm");

const predictButton =
    document.getElementById("predictButton");

const buttonText =
    document.getElementById("buttonText");

const resultBox =
    document.getElementById("result");

const predictionText =
    document.getElementById("predictionText");

const predictionMessage =
    document.getElementById("predictionMessage");

const confidenceText =
    document.getElementById("confidence");

const confidenceBox =
    document.getElementById("confidenceBox");

const resultIcon =
    document.getElementById("resultIcon");


form.addEventListener("submit", async function(event) {

    event.preventDefault();


    // Get data from HTML

    const data = {

        duration_sec:
            document.getElementById("duration_sec").value,

        title_length:
            document.getElementById("title_length").value,

        thumbnail_face:
            document.getElementById("thumbnail_face").value,

        upload_hour:
            document.getElementById("upload_hour").value,

        tags_count:
            document.getElementById("tags_count").value,

        description_length:
            document.getElementById("description_length").value,

        subscriber_count:
            document.getElementById("subscriber_count").value,

        views:
            document.getElementById("views").value,

        likes:
            document.getElementById("likes").value,

        comments:
            document.getElementById("comments").value,

        shares:
            document.getElementById("shares").value,

        category:
            document.getElementById("category").value,

        upload_day:
            document.getElementById("upload_day").value

    };


    // Change button text

    predictButton.disabled = true;

    buttonText.innerText =
        "Analyzing Video...";


    try {

        // Send data to Flask

        const response = await fetch("/predict", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(data)

        });


        const result =
            await response.json();


        // If prediction successful

        if (result.success) {


            // Show result box

            resultBox.classList.remove("hidden");


            // Prediction text

            predictionText.innerText =
                result.prediction;


            // Prediction message

            predictionMessage.innerText =
                result.message;


            // Change icon

            if (
                result.prediction.includes("Viral")
                &&
                !result.prediction.includes("Not")
            ) {

                resultIcon.innerText = "🔥";

            }

            else {

                resultIcon.innerText = "📊";

            }


            // Confidence

            if (
                result.confidence !== null
                &&
                result.confidence !== undefined
            ) {

                confidenceBox.style.display =
                    "inline-flex";

                confidenceText.innerText =
                    result.confidence + "%";

            }

            else {

                confidenceBox.style.display =
                    "none";

            }


            // Scroll to result

            resultBox.scrollIntoView({

                behavior: "smooth",

                block: "center"

            });

        }


        // If error

        else {

            alert(

                "Prediction Error: "
                +
                result.error

            );

        }

    }


    catch (error) {

        console.error(error);

        alert(
            "Something went wrong. Please try again."
        );

    }


    finally {

        // Enable button again

        predictButton.disabled = false;

        buttonText.innerText =
            "Predict Video Performance";

    }

});
