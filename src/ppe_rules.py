"""
ppe_rules.py

This module evaluates PPE compliance for detected workers.
"""

from detection import Detection


class PPERules:
    """
    Evaluates PPE compliance for tracked workers.
    """

    def __init__(self):
        print("PPE Rule Engine initialized.")

    def is_inside(self, person_bbox, object_bbox):
        """
        Checks whether the center of an object lies inside
        a person's bounding box.

        Parameters
        ----------
        person_bbox : tuple
            (x1, y1, x2, y2)

        object_bbox : tuple
            (x1, y1, x2, y2)

        Returns
        -------
        bool
        """

        # Person coordinates
        px1, py1, px2, py2 = person_bbox

        # Object coordinates
        ox1, oy1, ox2, oy2 = object_bbox

        # Object center
        center_x = (ox1 + ox2) // 2
        center_y = (oy1 + oy2) // 2

        return (
            px1 <= center_x <= px2 and
            py1 <= center_y <= py2
        )

    def find_helmet(self, person, hardhats):
        """
        Returns True if a helmet belongs to the person.
        """

        for helmet in hardhats:

            if self.is_inside(
                person.bbox,
                helmet.bbox
            ):
                return True

        return False

    def find_vest(self, person, safety_vests):
        """
        Returns True if a safety vest belongs to the person.
        """

        for vest in safety_vests:

            if self.is_inside(
                person.bbox,
                vest.bbox
            ):
                return True

        return False
    
    def find_mask(self, person, masks):
        """
        Returns True if a face mask belongs to the person.
        """

        for mask in masks:

            if self.is_inside(
            person.bbox,
            mask.bbox
        ):
             return True

        return False 
    
    def evaluate_worker_status(self, worker):
        """
        Determines the PPE compliance status of a worker.

        Parameters
        ----------
        worker : dict
        Dictionary containing PPE information.

        Returns
        -------
        str
        PPE status of the worker.
        """

        violations = []

        # Helmet
        if not worker["helmet"]:
           violations.append("NO HARDHAT")

    # Safety Vest
        if not worker["vest"]:
            violations.append("NO SAFETY VEST")

    # Face Mask
        if not worker["mask"]:
            violations.append("NO MASK")

    # No violations
        if len(violations) == 0:
         return "SAFE"

    # Combine all violations
        return " | ".join(violations)

    def evaluate(self, detections):
        """
        Evaluate PPE compliance for the current frame.

        Parameters
        ----------
        detections : list[Detection]
            List of all detections in the current frame.

        Returns
        -------
        list
            PPE status for each detected person.
        """

        # -----------------------------
        # Separate detections by class
        # -----------------------------

        persons = []
        hardhats = []
        safety_vests = []
        masks = []

        no_hardhats = []
        no_safety_vests = []
        no_masks = []

        for detection in detections:

            if detection.class_name == "Person":
                persons.append(detection)

            elif detection.class_name == "Hardhat":
                hardhats.append(detection)

            elif detection.class_name == "Safety Vest":
                safety_vests.append(detection)

            elif detection.class_name == "Mask":
                masks.append(detection)

            elif detection.class_name == "NO-Hardhat":
                no_hardhats.append(detection)

            elif detection.class_name == "NO-Safety Vest":
                no_safety_vests.append(detection)

            elif detection.class_name == "NO-Mask":
                no_masks.append(detection)

        print("\n========== PPE SUMMARY ==========")
        print(f"Persons           : {len(persons)}")
        print(f"Hardhats          : {len(hardhats)}")
        print(f"Safety Vests      : {len(safety_vests)}")
        print(f"Masks             : {len(masks)}")
        print(f"NO-Hardhat        : {len(no_hardhats)}")
        print(f"NO-Safety Vest    : {len(no_safety_vests)}")
        print(f"NO-Mask           : {len(no_masks)}")
        print("=================================\n")

        # -----------------------------
        # Build worker information
        # -----------------------------

        worker_status = []

        for person in persons:

            worker = {
                "track_id": person.track_id,
                "person": person,
                "helmet": self.find_helmet(person, hardhats),
                "vest": self.find_vest(person, safety_vests),
                "mask": self.find_mask(person, masks),
                "status": "UNKNOWN"
            }

            worker["status"] = self.evaluate_worker_status(worker)

            worker_status.append(worker)

        print("\n========== Worker PPE Status ==========")

        for worker in worker_status:

            print(
                f"Worker {worker['track_id']}\n "
                f"Helmet: {worker['helmet']}\n"
                f"Vest: {worker['vest']}\n"
                f"Mask: {worker['mask']}\n"
                f"Status: {worker['status']}\n"
            )

        print("=======================================\n")

        return worker_status