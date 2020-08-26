

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

new_cient_fields();