fetch('/static/data/historia.json')
.then(response => response.json())
.then(data => {
    var timeline_json = data;
    window.timeline = new TL.Timeline('timeline-embed', timeline_json, { start_at_end: true, scale_factor: 4, font: "lustria-lato" });
})
.catch(error => console.error('Error:', error));