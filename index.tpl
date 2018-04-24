<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/responsive/2.2.1/css/responsive.dataTables.min.css">
    <title>Postfix LogViewer</title>

    <style>
            td.details-control {
              cursor: pointer;
              text-align: center;
            }
            td.details-control:before {
              content: "\2b";
            }
            tr.shown td.details-control:before {
              content: "\2212";
            }
    </style>
</head>

<body>
    <table id="logtable" class="display nowrap" style="width:100%">
        <thead>
            <tr>
                <th></th>
                <th>#ID</th>
                <th>Datum</th>
                <th>Sender</th>
                <th>Empfänger</th>
                <th>Score</th>
            </tr>
        </thead>
        <tbody>
            <tr  id="loading_data">
                <td>Loding data....</td>
            </tr>
        </tbody>
    </table>

    <script src="http://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <script src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.16/js/dataTables.bootstrap4.min.js"></script>

    <script>
        $(document).ready(function() {
        var table = undefined;
        $.ajax({
            type: "GET",
            url: "/data",
            success: function(result) {
                data = [];
                $.each(result, function(index) {
                    if (this.relay === "dovecot" || this.server == null) return;
                    this["index"] = index;
                    data.push(this);
                });
                $("#loading_data").remove();
                table = $("#logtable").DataTable({
                    responsive: true,
                    order: [1, "desc"],
                    columns: [{
                        className: "details-control",
                        defaultContent: "",
                        data: null,
                        orderable: false
                    }, {
                        data: "index"
                    }, {
                        data: "date"
                    }, {
                        data: "sender"
                    }, {
                        data: "recipient"
                    }, {
                        data: "score"
                    }],
                    data: data
                });
            }
        });

        
          function format (data) {
              return "<div class='details-container'>"+
                  "<table cellpadding='5' cellspacing='0' border='0' class='details-table'>"+
                      "<tr>"+
                          "<td>Message-ID:</td>"+
                          "<td>"+data.id+"</td>"+
                      "</tr>"+
                        "<tr>"+
                          "<td>Server:</td>"+
                          "<td>"+data.server + "</td>"+
                      "</tr>"+
                      "<tr>"+
                          "<td>Status:</td>"+
                          "<td>"+data.status_extended + "</td>"+
                      "</tr>"+
                      "<tr>"+
                          "<td>Relay:</td>"+
                          "<td>"+data.relay+"</td>"+
                      "</tr>"+
                  "</table>"+
                "</div>";
          };
        
        $("#logtable tbody").on("click", "td.details-control", function() {
            var tr = $(this).closest("tr"),
                row = table.row(tr);

            if (row.child.isShown()) {
                tr.next("tr").removeClass("details-row");
                row.child.hide();
                tr.removeClass("shown");
            } else {
                row.child(format(row.data())).show();
                tr.next("tr").addClass("details-row");
                tr.addClass("shown");
            }
        });

        });

    </script>
</body>

</html>