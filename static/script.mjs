import dayjs from "./dayjs.min.mjs";
import relativeTime from "./dayjs.relativeTime.min.mjs";
import utc from "./dayjs.utc.min.mjs";
dayjs.extend(relativeTime);
dayjs.extend(utc);
setInterval(function() {
  document.querySelectorAll("time[data-arrival-time]").forEach(time => {
    const offset = dayjs(time.getAttribute("datetime")).diff(dayjs.utc(), 'm');

    if (offset <= 0) {
      time.innerText = "due";
    } else {
      time.querySelector(".arrival-time-mins").innerText = offset;
      if (offset < 5) {
        time.classList.add("arrival-time-due");
      }
    }
  });
  document.querySelectorAll("time[data-replace]").forEach(time => {
    const offsetSecs = dayjs(time.getAttribute("datetime")).diff(dayjs.utc(), 's')
    if (offsetSecs > -5) {
      time.innerText = 'just now';
    } else if (offsetSecs > -60) {
      time.innerText = `${Math.abs(offsetSecs)} seconds ago`;
    } else {
      time.innerText = dayjs(time.getAttribute("datetime")).fromNow();
    }
  })
}, 1000);


document.querySelector("a[data-all-stations-btn]").addEventListener("click", function(evt) {
  evt.preventDefault();

  const href = new URL(evt.target.href);
  href.searchParams.append("embed", "true")

  // TODO write a URL manipulation library that is actually good
  const iframe = document.querySelector("iframe[data-all-stations-frame]");
  iframe.src = href;
  iframe.addEventListener("load", function() {
    document.querySelector("dialog[data-all-stations-dialog]").showModal();
  }, { once: true });
})
