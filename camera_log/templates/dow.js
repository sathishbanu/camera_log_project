<!-- Download Button -->
        <div class="mb-3">
            <button class="btn btn-primary" onclick="downloadTable()">Download as CSV</button>
        </div>

// Download Table as CSV
        function downloadTable() {
            var rows = document.querySelectorAll('table tr');
            var csv = [];

            for (var i = 0; i < rows.length; i++) {
                var row = [];
                var cols = rows[i].querySelectorAll('td, th');

                for (var j = 0; j < cols.length; j++) {
                    row.push(cols[j].innerText);
                }
                csv.push(row.join(','));
            }

            // Create a CSV Blob and download it
            var csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
            var downloadLink = document.createElement('a');
            downloadLink.href = URL.createObjectURL(csvFile);
            downloadLink.download = 'camera_status_list.csv';
            downloadLink.click();
        }