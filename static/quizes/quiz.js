const url = window.location.href

const quizBox = document.getElementById("quiz-box")

function callSubmit() {      
    document.forms[0].submit();
}
// Set the date we're counting down to
var a = document.getElementById("datefin").value
console.log(a)
var countDownDate2 = new Date(a).getTime();
console.log(countDownDate2.toString())


var countDownDate = new Date("Jan 5, 2024 15:37:25").getTime();
console.log(countDownDate.toString())


// Update the count down every 1 second
var x = setInterval(function() {
    
  // Get today's date and time
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countDownDate2 - now;

  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="demo"
  document.getElementById("timer").innerHTML =   hours + "h "
  + minutes + "m " + seconds + "s ";

  // If the count down is finished, write some text
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("timer").innerHTML = "EXPIRED";
    //document.getElementById("quiz-form").submit();
    
    var element = document.getElementById('submit_btn');  
    if (element) {  
        element.click();
    }
    return
  }
  
}, 1000);
$.ajax(
    {
        type: 'GET',
        url: `${url}data`,
        success: function (response) {
            // console.log(response)
            const data = response.data
            const data2 = response.data2
            const data3 = response.data3
            console.log(data2)
            console.log(data)
            console.log(data3)

            data2.forEach(el => {
                for (const [question, reponses] of Object.entries(el)) {
                    quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>   
                    `

                    reponses.forEach(reponse => {
                        quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${reponse}" name="${question}" value="${reponse}" >
                            <label for="${question}">${reponse}</label>
                        </div>
                        `

                    })
                }
            })

            data.forEach(el => {
                for (const [question, reponses] of Object.entries(el)) {
                    quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>   
                    `

                    reponses.forEach(reponse => {
                        quizBox.innerHTML += `
                        <div>
                            <input type="checkbox" class="ans" id="${question}-${reponse}" name="${question}" value="${reponse}" >
                            <label for="${question}">${reponse}</label>
                        </div>
                        `

                    })
                }
            })
           

        },
        error: function (err) {
            console.log(error)
        }
    }
)

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    values = []
    var x = ""
    elements.forEach(el => {
        if (x != el.name) {
            values = []
        }
        if (el.checked) {
            console.log(el.name)
            values.push(el.value)
            data[el.name] = values
            console.log(data[el.name])
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
        x = el.name
    })
    $.ajax(
        {
            type: 'POST',
            url: `${url}save/`,
            data: data,
            success: function (response) {
                console.log("aaaaaaaaaaaaa")
                console.log(data)
                window.location.href = 'http://127.0.0.1:8000/c/mytests';
                console.log(response)
            },
            error: function (error) {
                console.log("errorrr")
                console.log(error)
            }
        }
    )


}

quizForm.addEventListener('submit', e => {
    e.preventDefault()
    sendData()
})

