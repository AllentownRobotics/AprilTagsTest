// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.math.controller.PIDController;
import frc.robot.Constants;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.Constants;
import frc.robot.RobotContainer;
import frc.robot.subsystems.VisionSub;

public class MoveToTag extends CommandBase {
  double y;
  double dis;
  PIDController pidController;
  /** Creates a new MoveToTag. */
  public MoveToTag() {
    pidController = new PIDController(0.01,0,0);
    pidController.setSetpoint(40);
    pidController.setTolerance(.5);
    addRequirements(RobotContainer.visionSubsystem);
    // Use addRequirements() here to declare subsystem dependencies.
  }

  // Called when the command is initially scheduled.
  @Override
  public void initialize() {}

  // Called every time the scheduler runs while the command is scheduled.
  @Override
  public void execute() {

    dis = RobotContainer.visionSubsystem.getDistance();
    //double distanceFromLimelightToGoalInches = (Constants.goalHeightInches - Constants.limelightLensHeightInches)/Math.tan(angleToGoalRadians);
    RobotContainer.drivetrainsubsystem.turnToTag(pidController.calculate(dis));

  }

  // Called once the command ends or is interrupted.
  @Override
  public void end(boolean interrupted) {}

  // Returns true when the command should end.
  @Override
  public boolean isFinished() {
    return false;
  }
}
