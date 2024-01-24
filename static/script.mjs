import dayjs from "./dayjs.min.mjs";
import relativeTime from "./dayjs.relativeTime.min.mjs";
import utc from "./dayjs.utc.min.mjs";
dayjs.extend(relativeTime);
dayjs.extend(utc);
setInterval(function() {
  document.querySelectorAll("time:not(.replace)").forEach(time => {
    const offset = dayjs(time.getAttribute("datetime")).diff(dayjs.utc(), 'm');
    time.querySelector(".arrival-time-mins").innerText = offset;

    if (offset === 0) {
      time.innerText = "due";
    } else if (offset < 5) {
      time.classList.add("arrival-time-due");
    }
  });
  document.querySelectorAll("time.replace").forEach(time => {
    const offsetSecs = dayjs(time.getAttribute("datetime")).diff(dayjs.utc(), 's')
    if (offsetSecs < 60) {
      time.innerText = `${offsetSecs} ago`;
    }
    time.innerText = dayjs(time.getAttribute("datetime")).fromNow();
  })
}, 1000);
