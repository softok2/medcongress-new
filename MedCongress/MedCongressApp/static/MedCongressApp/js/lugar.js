    var geocoder;
    var map1;
    var marker;


    function initialize(PostCodeid,lonid,latid) {
        var initialLat = $(latid).val();
        var initialLong = $(lonid).val();
        initialLat = initialLat ? initialLat : 0;
        initialLong = initialLong ? initialLong : 0;

        var latlng = new google.maps.LatLng(initialLat, initialLong);
        var options = {
            zoom: 11,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        map1 = new google.maps.Map(document.getElementById("geomap"), options);

        geocoder = new google.maps.Geocoder();

        marker = new google.maps.Marker({
            map: map1,
            draggable: true,
            position: latlng
        });

        google.maps.event.addListener(marker, "dragend", function () {
            var point = marker.getPosition();
            map1.panTo(point);
            geocoder.geocode({ 'latLng': marker.getPosition() }, function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    map1.setCenter(results[0].geometry.location);
                    marker.setPosition(results[0].geometry.location);
                    $(PostCodeid).val(results[0].formatted_address);
                    $(latid).val(marker.getPosition().lat());
                    $(lonid).val(marker.getPosition().lng());
                }
            });
        });

    }

    function FiltrarLugar(PostCodeid,lonid,latid){
        //load google map
        initialize(PostCodeid,lonid,latid);

        /*
         * autocomplete location search
         */
        $(function () {
            $(PostCodeid).autocomplete({
                source: function (request, response) {
                    geocoder.geocode({
                        'address': request.term
                    }, function (results, status) {
                        response($.map(results, function (item) {
                            return {
                                label: item.formatted_address,
                                value: item.formatted_address,
                                lat: item.geometry.location.lat(),
                                lon: item.geometry.location.lng(),

                            };
                        }));
                    });
                },
                select: function (event, ui) {


                    $(PostCodeid).val(ui.item.value);

                    $(latid).val(ui.item.lat);
                    $(lonid).val(ui.item.lon);

                    var latlng = new google.maps.LatLng(ui.item.lat, ui.item.lon);
                    marker.setPosition(latlng);
                    initialize(PostCodeid,lonid,latid);
                }
            });
        });

    }