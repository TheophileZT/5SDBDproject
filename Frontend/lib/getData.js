//////////////// Mock functions to sent stations JSON //////////////////////////

export async function getData(time) {
  // Simulate delay using a Promise
  await new Promise((resolve) => setTimeout(resolve, 2000));

  const hour3 = new Date();
  hour3.setHours(hour3.getHours() + 3);
  console.log(" Hours 3 : ", hour3);
  console.log(" Time: ", time);

  const data = [ [
    {
    lat: 43.609022,
    lng: 1.459063,
    nb_bike: 15,
    status_bike: 0,
    },
    {
    lat: 43.587323,
    lng: 1.437386,
    nb_bike: 8,
    status_bike: 0,
    },
    {
    lat: 43.600614,
    lng: 1.372218,
    nb_bike: 3,
    status_bike: 0,
    },
    {
    lat: 43.605899,
    lng: 1.463601,
    nb_bike: 6,
    status_bike: 0,
    },
    {
    lat: 43.615273,
    lng: 1.442937,
    nb_bike: 13,
    status_bike: 0,
    },
    {
    lat: 43.632734,
    lng: 1.431732,
    nb_bike: 13,
    status_bike: 0,
    },  
  ], [
    {
    lat: 43.620000,
    lng: 1.457063,
    nb_bike: 15,
    status_bike: 0,
    },
    {
    lat: 43.545323,
    lng: 1.437386,
    nb_bike: 8,
    status_bike: 1,
    },
    {
    lat: 43.60700,
    lng: 1.372218,
    nb_bike: 3,
    status_bike: 5,
    },
    {
    lat: 43.605000,
    lng: 1.463201,
    nb_bike: 6,
    status_bike: 4,
    },
    {
    lat: 43.615273,
    lng: 1.432937,
    nb_bike: 13,
    status_bike: 2,
    },
    {
    lat: 43.633004,
    lng: 1.431732,
    nb_bike: 13,
    status_bike: 3,
    },  
]]
  return JSON.stringify( (time <= hour3)? data[0] : data[1]);
  }
////////////////////////////////////////////////////////////////////////////////////////////////////////
