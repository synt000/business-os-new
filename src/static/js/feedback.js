console.log("FEEDBACK JS LOADED");


const modal = document.getElementById("feedbackModal");
const title = document.getElementById("feedbackTitle");
const subject = document.getElementById("feedbackSubject");
const message = document.getElementById("feedbackMessage");

let currentFeedbackType = "general";


function openFeedback(type){

    currentFeedbackType = type;

    if(!modal) return;


    modal.style.display="flex";


    if(type==="bug"){
        title.innerText="🐞 Report Bug";
        subject.value="Bug Report";
    }


    if(type==="feature"){
        title.innerText="💡 Suggest Feature";
        subject.value="Feature Request";
    }


    if(type==="rate"){
        title.innerText="⭐ Rate Experience";
        subject.value="User Feedback";
    }


    message.value="";

}



document
.getElementById("reportBugBtn")
?.addEventListener(
"click",
()=>openFeedback("bug")
);



document
.getElementById("featureBtn")
?.addEventListener(
"click",
()=>openFeedback("feature")
);



document
.getElementById("rateBtn")
?.addEventListener(
"click",
()=>openFeedback("rate")
);



document
.querySelector(".feedback-close")
?.addEventListener(
"click",
()=>{

    modal.style.display="none";

}
);



// Send Feedback (Beta Version)

document
.querySelector(".feedback-submit")
?.addEventListener(
"click",
()=>{


    const data = {

        feedback_type: currentFeedbackType,

        subject: subject.value,

        message: message.value

    };


    fetch("/api/v4/feedback", {

        method:"POST",

        headers:{
            "Content-Type":"application/json",
            "Authorization":
            "Bearer " + localStorage.getItem("access_token")
        },

        body:JSON.stringify(data)

    })

    .then(r=>r.json())

    .then(d=>{

        console.log("FEEDBACK RESPONSE =", d);

        alert("✅ Feedback sent");

        modal.style.display="none";

    })

    .catch(err=>{

        console.error(err);

        alert("❌ Feedback failed");

    });


}
);


