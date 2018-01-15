use std::f64;
use std::f64::NAN;

// rewritten 'as-is' from Go package github.com/asmarques/geodist
// https://github.com/asmarques/geodist/blob/master/vincenty.go
fn vincenty_distance(lat1: f64, lon1: f64, lat2: f64, lon2: f64) -> f64 {

	let a: f64 = 6378137.0;
	let f: f64 = 1.0/298.257223563;
	let b: f64 = 6356752.314245;

	let epsilon: f64 = 1e-12;
	let max_iterations: i32 = 200;

	if lat1 == lat2 && lon1 == lon2 {
		return 0.0;
	}

	let u1: f64 = ((1.0 - f) * lat1.to_radians().tan()).atan();
	let u2: f64 = ((1.0 - f) * lat2.to_radians().tan()).atan();
	let ll: f64 = (lon2 - lon1).to_radians();

	let sin_u1 = u1.sin();
	let cos_u1 = u1.cos();
	let sin_u2 = u2.sin();
	let cos_u2 = u2.cos();
	let mut lambda = ll;

	let mut result = NAN;

	for _i in 0..max_iterations {
		let cur_lambda = lambda;
		let sin_sigma = ((cos_u2*lambda.sin()).powi(2) + (cos_u1*sin_u2-sin_u1*cos_u2*lambda.cos()).powi(2)).sqrt();
		let cos_sigma = sin_u1*sin_u2 + cos_u1*cos_u2*lambda.cos();
		let sigma = sin_sigma.atan2(cos_sigma);
		let sin_alpha = (cos_u1 * cos_u2 * lambda.sin()) / sigma.sin();
		let cos_sqr_alpha = 1.0 - sin_alpha.powi(2);
		let mut cos2sigmam = 0.0;

		if cos_sqr_alpha != 0.0 {
			cos2sigmam = sigma.cos() - ((2.0 * sin_u1 * sin_u2) / cos_sqr_alpha);
		}

		let cc = (f / 16.0) * cos_sqr_alpha * (4.0 + f*(4.0-3.0*cos_sqr_alpha));
		lambda = ll + (1.0-cc)*f*sin_alpha*(sigma+cc*sin_sigma*(cos2sigmam+cc*cos_sigma*(-1.0+2.0*cos2sigmam.powi(2))));

		if (lambda-cur_lambda).abs() < epsilon {
			let u_sqr = cos_sqr_alpha * ((a.powi(2) - b.powi(2)) / b.powi(2));
			let k1 = ((1.0+u_sqr).sqrt() - 1.0) / ((1.0+u_sqr).sqrt() + 1.0);
			let aa = (1.0 + (k1.powi(2) / 4.0)) / (1.0 - k1);
			let bb = k1 * (1.0 - (3.0*k1.powi(2))/8.0);
			let delta_sigma = bb * sin_sigma * (cos2sigmam + (bb/4.0)*(cos_sigma*(-1.0+2.0*cos2sigmam.powi(2))-(bb/6.0)*cos2sigmam*(-3.0+4.0*sin_sigma.powi(2))*(-3.0+4.0*cos2sigmam.powi(2))));
			let s = b * aa * (sigma - delta_sigma);
			result = s / 1000.0;
			break
		}
	}

	return result;

 }

#[no_mangle]
pub extern fn rust_distance(lat1: f64, lon1: f64, lat2: f64, lon2: f64) -> f64 {
	let res = vincenty_distance(lat1, lon1, lat2, lon2);
	return (res*10000.0).round()/10000.0;
}

// fn main() {
// 	// 347.3727
//  	// println!("{}", rust_distance(52.2296756, 22.0122287, 52.406374, 16.9251681));
//  }