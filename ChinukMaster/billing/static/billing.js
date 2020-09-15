var new_cient_fields = function() {

    let treners = document.getElementById('id_treners');
    let groups = document.getElementById('id_groups');

    let cl_type = document.getElementById('id_cl_type');
    cl_type.addEventListener('change', () => {
        if (cl_type.value == 'I') {
            treners.style.display = 'block';
            groups.style.display = 'none';
        } else if (cl_type.value == 'G') {
            treners.style.display = 'none';
            groups.style.display = 'block';
        } else {
            treners.style.display = 'block';
            groups.style.display = 'block';
        }
    });
};

var new_payment_fields = function() {

    let payment_to = document.getElementById('id_payment_to');
    let trener_part = document.getElementById('id_trener_part');
    let trener = document.getElementById('id_trener');
    let group = document.getElementById('id_group');

    payment_to.addEventListener('change', () => {
        if (payment_to.value == 'I') {
            trener_part.style.display = 'block';
            trener.style.display = 'block';
            group.style.display = 'none';
        } else {
            trener_part.style.display = 'none';
            trener.style.display = 'none';
            group.style.display = 'block';
        };
    });

};

function MAIN() {

    title = document.getElementById('title').innerHTML;
    
    if (title == 'New payment') {
        new_payment_fields();
    } else if (title == 'New client') {
        new_cient_fields();
    }
};

MAIN();