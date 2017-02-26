//
//  ViewController.swift
//  wander
//
//  Created by Eskandary, Nima on 2/25/17.
//  Copyright © 2017 Eskandary, Nima. All rights reserved.
//

import UIKit
import Alamofire
import CoreLocation

class ViewController: UIViewController, CLLocationManagerDelegate {
    
    var locationManager:CLLocationManager!
    var backgroundTaskIdentifier: UIBackgroundTaskIdentifier?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        
        // used to make keyboard go away when clicking screen
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(ViewController.dismissKeyboard))
        
        view.addGestureRecognizer(tap)
    }
    
    
    func determineMyCurrentLocation() {
        locationManager = CLLocationManager()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.requestAlwaysAuthorization()
        
        if CLLocationManager.locationServicesEnabled() {
            locationManager.startUpdatingLocation()
            //locationManager.startUpdatingHeading()
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        let userLocation:CLLocation = locations[0] as CLLocation
        
        // Call stopUpdatingLocation() to stop listening for location updates,
        // other wise this function will be called every time when user location changes.
        
        // manager.stopUpdatingLocation()
        savedLoc = [userLocation.coordinate.latitude, userLocation.coordinate.longitude]
        print("user latitude = \(userLocation.coordinate.latitude)")
        print("user longitude = \(userLocation.coordinate.longitude)")
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error)
    {
        print("Error \(error)")
    }
    
    //Calls this function when the tap is recognized.
    func dismissKeyboard() {
        //Causes the view (or one of its embedded text fields) to resign the first responder status.
        view.endEditing(true)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    //MARK: Scope
    
    var groupName: String = ""
    var groupCode: String = ""
    var hardCodedGroup: String = "DFFH"
    
    var savedDisplayName: String = ""
    var savedGroupCode: String = ""
    var savedLoc = [50.0,50.0]
    
    //MARK: Join Group Properties
    
    @IBOutlet weak var joinName: UITextField!
    @IBOutlet weak var joinCode: UITextField!
    
    @IBOutlet weak var testlabel: UILabel!
    
    //MARK: Join Group Actions
    
    @IBAction func joinGroup(_ sender: Any) {
        let url = "http://23.96.125.188:5000/joinGroup/" + joinCode.text!
        let parameters: Parameters = [
            "dispName": joinName.text!
        ]
        Alamofire.request(url, method: .post, parameters: parameters, encoding: JSONEncoding.default)
        groupCode = joinCode.text!
    
        backgroundTaskIdentifier = UIApplication.sharedApplication().beginBackgroundTaskWithExpirationHandler({
            UIApplication.sharedApplication().endBackgroundTask(self.backgroundTaskIdentifier!)
        })
        var timer = Timer.scheduledTimer(timeInterval: 10, target: self, selector: #selector(self.pushLocation), userInfo: nil, repeats: true)
    }
    
    func pushLocation() {
        print("test")
        determineMyCurrentLocation()
        print (savedLoc)
        let url = "http://23.96.125.188:5000/updateLoc"
        let parameters: Parameters = [
            "dispName": savedDisplayName,
            "groupCode": savedGroupCode,
            "loc": savedLoc
        ]
        Alamofire.request(url, method: .post, parameters: parameters, encoding: JSONEncoding.default)
    }
    
    
    //MARK: Create Group Properties
    
    @IBOutlet weak var createThreshold: UITextField!
    @IBOutlet weak var createName: UITextField!
    @IBOutlet weak var createGroupName: UITextField!
    
    @IBOutlet weak var codeDisplay: UILabel!
    @IBOutlet weak var testCreateLabel: UILabel!
    
    //MARK: Create Group Actions
    
    @IBAction func createGroup(_ sender: Any) {
        let url = "http://23.96.125.188:5000/createGroup"
        let parameters: Parameters = [
            "groupName": createGroupName.text!,
            "dispName": createName.text!,
            "triggerDist": createThreshold.text!
            
        ]
        Alamofire.request(url, method: .post, parameters: parameters, encoding: JSONEncoding.default).responseJSON { response in
            
            if let result = response.result.value {
                let JSON = result as! NSDictionary
                print (JSON)
                self.groupCode = JSON.object(forKey: "groupCode") as! String
            }
        }
    }
    
    
    
    
    //MARK: Actions
    
    /* @IBAction func joinGroupClick(_ sender: Any) {
        Alamofire.request("https://google.com").responseString { response in
            self.joinGroupDisplayNameInput.text = response.value
        }
        
    } */
    
    
}

