// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import com.revrobotics.CANSparkMax;
import com.revrobotics.SparkMaxPIDController;
import com.revrobotics.CANSparkMaxLowLevel.MotorType;

import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj.drive.DifferentialDrive;
import edu.wpi.first.wpilibj.motorcontrol.MotorControllerGroup;
import edu.wpi.first.wpilibj2.command.CommandBase;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.Constants;
public class DriveTrain extends SubsystemBase {
  //Define motor variables
  private CANSparkMax leftLead;
  private CANSparkMax leftFollow;
  private CANSparkMax rightLead;
  private CANSparkMax rightFollow;
  private DifferentialDrive driver;
  private MotorControllerGroup left;
  private MotorControllerGroup right;

  public DriveTrain() {

    //Set motors
    leftLead = new CANSparkMax(Constants.leftLeadid, MotorType.kBrushless);
    leftFollow = new CANSparkMax(Constants.leftFollowid, MotorType.kBrushless);
    rightLead = new CANSparkMax(Constants.rightLeadid, MotorType.kBrushless);
    rightFollow = new CANSparkMax(Constants.rightFollowid, MotorType.kBrushless);

    //Set motor control groups
    left = new MotorControllerGroup(leftLead, leftFollow);
    right = new MotorControllerGroup(rightLead, rightFollow);

    left.setInverted(true);
    driver = new DifferentialDrive(left, right);
  }
  @Override
  public void periodic() {
    // This method will be called once per scheduler run
  }
  public void drive(XboxController controller){
    driver.arcadeDrive(controller.getLeftY()*Constants.driveMultiplier,controller.getRightX()*Constants.driveMultiplier);
  }

  public void turnToTag(double speed)
  {
    left.set(speed);
    right.set(-speed);
  }
  public void MoveToTag(double speed)
  {
    left.set(speed);
    right.set(-speed);
  }

}
