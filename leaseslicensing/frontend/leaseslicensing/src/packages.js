import moment from 'moment';
import { extendMoment } from 'moment-range';
import jszip from 'jszip';
/*
require( 'datatables.net' )();
require( 'datatables.net-bs5' )();
require( 'datatables.net-responsive-bs' )(window, $);
require( 'datatables.net-buttons/js/dataTables.buttons.js' )(window, $);
require( 'datatables.net-buttons/js/buttons.html5.js' )(window, $, jszip);

require("datatables.net-bs/css/dataTables.bootstrap.css");
require("datatables.net-responsive-bs/css/responsive.bootstrap.css");

require("sweetalert2/dist/sweetalert2.css");

require('jquery-validation');
*/

import 'datatables.net';
import 'datatables.net-bs5';
import 'datatables.net-responsive-bs';
import 'datatables.net-buttons';

import "sweetalert2";

import 'jquery-validation';

extendMoment(moment);

