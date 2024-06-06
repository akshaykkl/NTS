document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('toggle-edit-mode');
    const table = document.getElementById('media-table');
    const actionHeader = table.querySelector('th.action-column');
    const actionCells = table.querySelectorAll('td.action-column');

    toggleButton.addEventListener('click', function () {
        if (actionHeader.style.display === 'none') {
            actionHeader.style.display = '';
            actionCells.forEach(function (cell) {
                cell.style.display = '';
            });
        } else {
            actionHeader.style.display = 'none';
            actionCells.forEach(function (cell) {
                cell.style.display = 'none';
            });
        }
    });

    // Initially hide the action column
    actionHeader.style.display = 'none';
    actionCells.forEach(function (cell) {
        cell.style.display = 'none';
    });
});
