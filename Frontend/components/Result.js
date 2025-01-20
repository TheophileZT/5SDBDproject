export default function Result({ prediction }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto mt-4 mb-1">
      <h2 className="text-2xl font-semibold mb-4 text-center">Prediction Result</h2>
      <p className="text-xl text-gray-800 text-center">
        Predicted number of bikes: 
        <span className="font-bold text-indigo-600">{prediction}</span>
      </p>
    </div>
  );
}


/** Prediction results
 * 
 * Plus proche station
 * Nombre de vélo
 * Status
 * 
 * Accuracy ?
 */