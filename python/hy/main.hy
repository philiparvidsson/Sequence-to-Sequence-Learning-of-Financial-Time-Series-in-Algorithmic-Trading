#!/usr/bin/env hy

;;;-------------------------------------
;;; IMPORTS
;;;-------------------------------------

(import [math]
        [matplotlib]
        [pandas     :as pd]
        [tensorflow :as tf])

;;;-------------------------------------
;;; CONSTANTS
;;;-------------------------------------

(def data-file "EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv")

;;; Model configuration.
(def num-cells      (, 3 128 3)
     num-classes    3
     num-iterations 100
     window-size    5)                  ; Window size is in minutes.

;;; Class labels and their values.
(def y-down      (, 1 0 0)
     y-up        (, 0 1 0)
     y-unchanged (, 0 0 1)
     y-threshold 0.0000001)

;;;-------------------------------------
;;; FUNCTIONS
;;;-------------------------------------

(defn calc-x [data]
  (let [xs []]
    (for [x (. data values)]
      (if (any (map math.isnan x))
        (raise (Exception "Data must not contain NaN values.")))

      (.append xs x))
    xs))

(defn calc-y [xs]
  (let [ys []]
    (for [x xs]
      (let [c (. x [3])
            o (. x [0])
            d (- c o)
            y (if (<  (abs d)    y-threshold)  y-unchanged
                  (<=      d  (- y-threshold)) y-down
                  (>=      d     y-threshold)  y-up
                  (raise (Exception "Something is wrong with the data")))]
        (.append ys y)))
    ys))

(defn load-data [fn]
  "Loads finance data from the specified CSV file."
  (pd.read-csv fn :index-col "Time" :parse-dates ["Time"]))

(defn create-model [x y]
  (let [session (tf.Session)
        ]))

;;;-------------------------------------
;;; ENTRY POINT
;;;-------------------------------------

(defmain [&rest args]
  (let [df           (load-data data-file)
        df-1min-ohlc (-> df (.resample "1Min") .ohlc)
        asks         (.fillna (get df-1min-ohlc "Ask") :method "ffill")]

    ;; Add a timestamp column to the data.
    (assoc asks "time" (.map (. asks index) matplotlib.dates.date2num))

    (let [x (calc-x asks)
          y (calc-y x)]
      (create-model x y)))
