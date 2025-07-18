function greet()
{
    alert('Hello ' + document.querySelector('#name').value + '! I hope you have an amazing day!');
}

function changeBodyColor(event)
{
    let body = document.querySelector('body');
    let trigger = event.srcElement;
    body.style.backgroundColor = trigger.innerHTML.toLowerCase();
}

function changeHeaderColor(event)
{
    let header = document.querySelector('.nav');
    let trigger = event.srcElement;
    header.style.backgroundColor = trigger.innerHTML.toLowerCase();
}

function checkMC(event) {
    let button = event.target;
    if (button.innerHTML == 'Wellington') {
        button.style.backgroundColor = 'Green';
        button.parentElement.querySelector('.feedback1').innerHTML = 'Correct';
        button.parentElement.querySelector('.feedback1').style.color = 'green';
    }
    else {
        button.style.backgroundColor = 'Red';
        button.parentElement.querySelector('.feedback1').innerHTML = 'Incorrect';
        button.parentElement.querySelector('.feedback1').style.color = 'red';

    }
}

function checkFreeResponse(event) {
    let button = event.target;
    let input = document.querySelector('input');
    if (input.value == 'Sweden') {
        input.style.backgroundColor = 'Green';
        button.parentElement.querySelector('.feedback2').innerHTML = 'Correct';
        button.parentElement.querySelector('.feedback2').style.color = 'green';
    }
    else {
        input.style.backgroundColor = 'Red';
        button.parentElement.querySelector('.feedback2').innerHTML = 'Incorrect';
        button.parentElement.querySelector('.feedback2').style.color = 'red';
    }
}

function arithmetic()
{
    let num1 = document.querySelector('#num1').value;
    let num2 = document.querySelector('#num2').value;
    document.querySelector('#add').addEventListener('click', function() {
        sum = parseInt(num1) + parseInt(num2);
        alert("The sum is " + sum);
    })

    document.querySelector('#subtract').addEventListener('click', function() {
        difference = parseInt(num1) - parseInt(num2);
        alert("The difference is " + difference);
    })

    document.querySelector('#multiply').addEventListener('click', function() {
        product = parseInt(num1) * parseInt(num2);
        alert("The product is " + product);
    })

    document.querySelector('#divide').addEventListener('click', function() {
        quotient = parseInt(num1) / parseInt(num2);
        alert("The quotient is " + quotient);
    })
}

let random_num = Math.floor(Math.random() * (101 - 1 + 1) + 1);

function guess_num(event, ans)
{
    let button = event.target;
    document.querySelector('#making').addEventListener('click', function() {
        let guess = document.querySelector('#guess').value;
        if (guess > ans)
        {
            button.parentElement.querySelector('.feedback3').innerHTML = 'Too high. Try again.';
        }
        else if (guess < ans)
        {
            button.parentElement.querySelector('.feedback3').innerHTML = 'Too low. Try again.';
        }
        else
        {
            button.parentElement.querySelector('.feedback3').innerHTML = 'Congratulations, you did it! Good job!';
        }
    })
}

function give_up(event, ans)
{
    let button = event.target;
    document.querySelector('#quit').addEventListener('click', function() {
        let string = "The answer is " + ans + ". Better luck next time!"
        button.parentElement.querySelector('.feedback3').innerHTML = string;
        document.querySelector('#making').style.cursor = 'not-allowed';
        document.querySelector('#making').style.opacity = 0.6;
    })
}
