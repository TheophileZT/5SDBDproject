import styles from './Input-Form.module.css';

export default function InputForm({ address, setAddress, time, setTime, handleSubmit }) {
    return (
      <div className={styles.boxform}>
        <form onSubmit={handleSubmit} className={styles.form}>
          <h2 className={styles.title}>Enter Details</h2>
          
          <div className={styles.inputContainer}>
          <input 
              id="address"
              className={styles.input}
              type="text" 
              value={address} 
              placeholder=" "
              onChange={(e) => setAddress(e.target.value)} 
              required 
            />
          <div className={styles.cut}></div>
          <label for="address" className={styles.placeholder}>Address</label>
        </div>
          
          <div className={styles.inputContainer}>
            <input 
              id="time"
              className={styles.input}
              type="datetime-local" 
              value={time} 
              placeholder=" "
              onChange={(e) => setTime(e.target.value)} 
              required
            />
            <div className={styles.cut}></div>
            <label for="time" className={styles.placeholder}>Time</label>
          </div>
          
          <button type="submit" className={styles.submit}>Get Prediction</button>
        </form>
      </div>
    );
  }
  