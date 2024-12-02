  // Funkcia na zobrazenie alebo skrytie priest_list
  function togglePriest_list() {
    const priest_listDiv = document.getElementById('priest_list');
    priest_listDiv.style.display = (priest_listDiv.style.display === 'none') ? 'block' : 'none';
    if (priest_listDiv.style.display === 'block') {
      loadTimelineData();
    }
  }

  // Načítať údaje zo súboru JSON a zobraziť ich v tabuľke
  function loadTimelineData() {
    fetch('/static/data/historia.json')
      .then(response => response.json())
      .then(data => {
        const tableBody = document.getElementById('priest_list-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; // Vyčistiť predchádzajúci obsah

        data.events.forEach(event => {
          const row = tableBody.insertRow();

          // Formátovanie dátumu do dd.mm.yyyy
          const formatDate = (date) => {
            if (!date) return '';
            const day = date.day ? String(date.day).padStart(2, '0') : '01';
            const month = date.month ? String(date.month).padStart(2, '0') : '01';
            const year = date.year ? date.year : '';
            return `${day}.${month}.${year}`;
          };

          const startDate = formatDate(event.start_date);
          const endDate = formatDate(event.end_date);
          
          const yearsCell = row.insertCell(0);
          yearsCell.textContent = `${startDate} - ${endDate}`;

          // Mená a životopis
          const nameTextCell = row.insertCell(1);
          nameTextCell.innerHTML = `<strong>${event.text.headline}</strong><br>${event.text.text || ''}`;
        });
      })
      .catch(error => {
        console.error('Chyba pri načítavaní dát:', error);
      });
}
