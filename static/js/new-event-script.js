const lessonFormGroup = document.querySelector("#lessonFormGroup");
const unitEventFormGroup = document.querySelector("#unitEventFormGroup");
const formGroup = document.querySelector("#formGroup");

const eventTypeSelect = document.querySelector("#eventTypeSelect");

function onEventTypeSelected() {
    changeEventType(eventTypeSelect.value);
}

function changeEventType(type) {
    while (formGroup.lastElementChild) {
        formGroup.removeChild(formGroup.lastElementChild);
    }
    if (type === "lesson") {
        formGroup.append(lessonFormGroup.content.cloneNode(true));
    } else {
        formGroup.append(unitEventFormGroup.content.cloneNode(true));
    }
}

eventTypeSelect.addEventListener("change", onEventTypeSelected);

(() => {
    changeEventType(eventTypeSelect.value);
})();

