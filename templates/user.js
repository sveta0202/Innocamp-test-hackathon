const calendarGrid = document.getElementById("calendarGrid");
const currentMonthTitle = document.getElementById("currentMonth");
const prevBtn = document.getElementById("prevMonth");
const nextBtn = document.getElementById("nextMonth");
const viewButtons = document.querySelectorAll(".view-btn");

const addEventBtn = document.getElementById("voiceCommand");
const modal = document.getElementById("eventModal");
const closeModal = document.getElementById("closeModal");
const cancelEvent = document.getElementById("cancelEvent");
const eventForm = document.getElementById("eventForm");

let currentDate = new Date();
let currentView = "week";
let events = [];

const monthNames = [
  "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
  "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
];

const weekDays = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"];

function formatDate(date) {
  return date.toISOString().split("T")[0];
}

function updateTitle() {
  currentMonthTitle.textContent =
    `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
}

function renderCalendar() {
  calendarGrid.innerHTML = "";

  weekDays.forEach(day => {
    const dayHeader = document.createElement("div");
    dayHeader.className = "calendar-header-day";
    dayHeader.textContent = day;
    calendarGrid.appendChild(dayHeader);
  });

  if (currentView === "month") renderMonth();
  if (currentView === "week") renderWeek();
  if (currentView === "day") renderDay();

  updateTitle();
}

function renderMonth() {
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);

  let startDay = firstDay.getDay();
  startDay = startDay === 0 ? 6 : startDay - 1;

  const daysInMonth = lastDay.getDate();

  for (let i = 0; i < startDay; i++) {
    const emptyDay = document.createElement("div");
    emptyDay.className = "calendar-day other-month";
    calendarGrid.appendChild(emptyDay);
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month, day);
    createDayCell(date);
  }
}

function renderWeek() {
  const date = new Date(currentDate);
  const day = date.getDay();
  const mondayShift = day === 0 ? -6 : 1 - day;

  const monday = new Date(date);
  monday.setDate(date.getDate() + mondayShift);

  for (let i = 0; i < 7; i++) {
    const weekDate = new Date(monday);
    weekDate.setDate(monday.getDate() + i);
    createDayCell(weekDate);
  }
}

function renderDay() {
  for (let i = 0; i < 6; i++) {
    const emptyDay = document.createElement("div");
    emptyDay.className = "calendar-day other-month";
    calendarGrid.appendChild(emptyDay);
  }

  createDayCell(currentDate);
}

function createDayCell(date) {
  const dateString = formatDate(date);
  const todayString = formatDate(new Date());

  const dayCell = document.createElement("div");
  dayCell.className = "calendar-day";

  if (dateString === todayString) {
    dayCell.classList.add("today");
  }

  if (date.getMonth() !== currentDate.getMonth() && currentView === "month") {
    dayCell.classList.add("other-month");
  }

  dayCell.innerHTML = `
    <div class="day-number">${date.getDate()}</div>
    <div class="events-list"></div>
  `;

  const eventsList = dayCell.querySelector(".events-list");

  const dayEvents = events.filter(event => event.date === dateString);

  dayEvents.forEach(event => {
    const eventItem = document.createElement("div");
    eventItem.className = `event-item ${event.category}`;

    if (event.important) {
      eventItem.classList.add("important");
    }

    eventItem.textContent = `${event.time} ${event.title}`;
    eventsList.appendChild(eventItem);
  });

  calendarGrid.appendChild(dayCell);
}

prevBtn.addEventListener("click", () => {
  if (currentView === "month") {
    currentDate.setMonth(currentDate.getMonth() - 1);
  }

  if (currentView === "week") {
    currentDate.setDate(currentDate.getDate() - 7);
  }

  if (currentView === "day") {
    currentDate.setDate(currentDate.getDate() - 1);
  }

  renderCalendar();
});

nextBtn.addEventListener("click", () => {
  if (currentView === "month") {
    currentDate.setMonth(currentDate.getMonth() + 1);
  }

  if (currentView === "week") {
    currentDate.setDate(currentDate.getDate() + 7);
  }

  if (currentView === "day") {
    currentDate.setDate(currentDate.getDate() + 1);
  }

  renderCalendar();
});

viewButtons.forEach(button => {
  button.addEventListener("click", () => {
    viewButtons.forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");

    currentView = button.dataset.view;
    renderCalendar();
  });
});

addEventBtn.addEventListener("click", () => {
  modal.classList.add("active");
  document.getElementById("eventDate").value = formatDate(currentDate);
});

function closeEventModal() {
  modal.classList.remove("active");
  eventForm.reset();
}

closeModal.addEventListener("click", closeEventModal);
cancelEvent.addEventListener("click", closeEventModal);

eventForm.addEventListener("submit", function (e) {
  e.preventDefault();

  const newEvent = {
    title: document.getElementById("eventTitle").value,
    date: document.getElementById("eventDate").value,
    time: document.getElementById("eventTime").value,
    category: document.getElementById("eventCategory").value,
    location: document.getElementById("eventLocation").value,
    description: document.getElementById("eventDescription").value,
    important: document.getElementById("eventImportant").checked
  };

  events.push(newEvent);

  closeEventModal();
  renderCalendar();
});

renderCalendar();
