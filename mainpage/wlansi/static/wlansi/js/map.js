$(document).ready(function () {
    var icon = new google.maps.MarkerImage(
        // TODO: Very ugly, but it works
        'https://nodes.wlan-si.net/images/status_up_gmap.png',
        new google.maps.Size(20, 32),
        new google.maps.Point(0, 0),
        new google.maps.Point(9, 30)
    );
    var shadow = new google.maps.MarkerImage(
        // TODO: Very ugly, but it works
        'https://nodes.wlan-si.net/images/gmap_node_shadow.png',
        new google.maps.Size(32, 32),
        new google.maps.Point(0, 0),
        new google.maps.Point(9, 30)
    );
    var shape = {
        'coord': [12, 0, 14, 1, 15, 2, 16, 3, 16, 4, 16, 5, 17, 6, 17, 7, 17, 8, 16, 9, 16, 10, 16, 11, 15, 12, 14, 13, 13, 14, 14, 15, 14, 16, 15, 17, 15, 18, 16, 19, 16, 20, 16, 21, 17, 22, 17, 23, 18, 24, 18, 25, 19, 26, 19, 27, 15, 28, 16, 29, 14, 30, 5, 30, 3, 29, 4, 28, 0, 27, 1, 26, 1, 25, 1, 24, 2, 23, 2, 22, 3, 21, 3, 20, 4, 19, 4, 18, 4, 17, 5, 16, 5, 15, 6, 14, 5, 13, 4, 12, 3, 11, 3, 10, 3, 9, 2, 8, 2, 7, 2, 6, 3, 5, 3, 4, 3, 3, 4, 2, 5, 1, 7, 0],
        'type': 'poly'
    };
    var styles = [
        {
            'featureType': 'road',
            'stylers': [
                {
                    'visibility': 'off'
                }
            ]
        }
    ];
    var map_options = {
        'zoom': MAP_ZOOM,
        'center': new google.maps.LatLng(MAP_LATITUDE, MAP_LONGITUDE),
        'mapTypeId': google.maps.MapTypeId.ROADMAP,
        'styles': styles
    };
    var map = new google.maps.Map(document.getElementById('map_canvas'), map_options);
    $.each(nodes, function (i, node) {
        var marker = new google.maps.Marker({
            'position': new google.maps.LatLng(node.lat, node.long),
            'map': map,
            'shadow': shadow,
            'icon': icon,
            'shape': shape,
            'title': node.name
        });
        google.maps.event.addListener(marker, 'click', function () {
            document.location = node.url;
        });
    });
    function updateStatus() {
        var bounds = map.getBounds();
        var visible_nodes = 0;
        $.each(nodes, function (i, node) {
            if (bounds.contains(new google.maps.LatLng(node.lat, node.long))) visible_nodes++;
        });
        var fmts = ngettext("%(visible_nodes)s active node visible (%(all_nodes)s all)", "%(visible_nodes)s active nodes visible (%(all_nodes)s all)", visible_nodes);
        $('.map_status').text(interpolate(fmts, {
            'visible_nodes': visible_nodes,
            'all_nodes': nodes.length
        }, true));
    }
    google.maps.event.addListener(map, 'bounds_changed', updateStatus);
});