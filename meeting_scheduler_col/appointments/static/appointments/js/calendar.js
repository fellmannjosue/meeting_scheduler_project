$(document).ready(function () {
    const calendar = $('#calendar');
    const timeSlots = $('#time-slots');

    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDay = new Date(year, month, 1).getDay();

    // Generar encabezado del calendario
    calendar.append(`
        <thead>
            <tr>
                <th>Dom</th>
                <th>Lun</th>
                <th>Mar</th>
                <th>Mié</th>
                <th>Jue</th>
                <th>Vie</th>
                <th>Sáb</th>
            </tr>
        </thead>
    `);

    // Generar días del calendario
    let day = 1;
    const tbody = $('<tbody>');
    for (let i = 0; i < 6; i++) {
        const row = $('<tr>');
        for (let j = 0; j < 7; j++) {
            const cell = $('<td>');
            if (i === 0 && j < firstDay || day > daysInMonth) {
                cell.text('');
            } else {
                cell.text(day).addClass('day').data('date', `${year}-${month + 1}-${day}`);
                day++;
            }
            row.append(cell);
        }
        tbody.append(row);
    }
    calendar.append(tbody);

    // Manejar clic en un día
    $('.day').on('click', function () {
        $('.day').removeClass('selected');
        $(this).addClass('selected');
        const selectedDate = $(this).data('date');
        $('#selected-date').val(selectedDate);
        loadTimeSlots(selectedDate);
    });

    // Cargar horarios disponibles
    function loadTimeSlots(date) {
        const teacherId = $('#teacher-id').val();
        if (!teacherId) {
            alert('No se encontró el ID del maestro.');
            return;
        }

        $.ajax({
            url: "/appointments/get-available-slots/",
            method: 'GET',
            data: { date, teacher_id: teacherId },
            success: function (response) {
                timeSlots.empty();
                response.slots.forEach(slot => {
                    const timeSlot = $('<button>')
                        .addClass('btn btn-outline-primary w-100 time-slot')
                        .text(slot);
                    timeSlot.on('click', function () {
                        $('.time-slot').removeClass('selected');
                        $(this).addClass('selected');
                        $('#selected-time').val(slot);
                    });
                    timeSlots.append(timeSlot);
                });
            },
            error: function () {
                alert('Error al cargar los horarios disponibles.');
            }
        });
    }

    // Manejar la confirmación de la cita
    $('#appointment-form').on('submit', function (e) {
        e.preventDefault();
        const formData = $(this).serialize();

        $.ajax({
            url: "/appointments/confirm/",
            method: 'POST',
            data: formData,
            success: function () {
                $('#confirmation-modal').modal('show');
                $('#confirmation-modal').on('hidden.bs.modal', function () {
                    window.location.href = "/appointments/create/";
                });
            },
            error: function () {
                alert('Error al agendar la cita. Por favor, inténtelo de nuevo.');
            }
        });
    });

    // Redirigir al formulario al cerrar el modal
    $('#modal-accept').on('click', function () {
        $('#confirmation-modal').modal('hide');
        window.location.href = "/appointments/create/";
    });
});
