// Call the dataTables jQuery plugin
$(document).ready(function () {
    $('#dataTable').DataTable({
        paging: false,
        searching: false,
        info: false,
        ordering: false,
        autoWidth: false
    });
});
