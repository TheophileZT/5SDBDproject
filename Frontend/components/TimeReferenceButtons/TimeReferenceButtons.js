import { useState } from "react";
import styles from "./TimeReferenceButtons.module.css";

export default function TimeReferenceButtons( { onPredict }) {
  const [selectedTime, setSelectedTime] = useState(1); // Default to 1 hour

  const timeOptions = [1, 2, 3, 4, 5, 6];

  function handlePredictClick() {
  if (typeof onPredict === "function") {
    onPredict(selectedTime);
  } else {
    console.error("onPredict callback is not defined.");
  }
}
  return (
    <div>
      <div className={styles.card}>

        <div className={styles.buttonsContainer}>
          {timeOptions.map((time) => (
            <button
              key={time}
              className={`${styles.button} ${
                selectedTime === time ? styles.activeButton : ""
              }`}
              onClick={() => setSelectedTime(time)}
            >
              {time} Hour{time > 1 ? "s" : ""}
            </button>
          ))}
        </div>
        
        <p className={styles.selectedTime}>
          Select Time
        </p>
        <button
              className={`${styles.button} margin: 0 padding:0`}
              onClick={handlePredictClick}
            >
              Predict
            </button>
      </div>
    </div>
  );
}
