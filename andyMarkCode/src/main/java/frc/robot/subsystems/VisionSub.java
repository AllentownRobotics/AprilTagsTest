package frc.robot.subsystems;

import java.lang.reflect.Array;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableEntry;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj.shuffleboard.*;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

public class VisionSub extends SubsystemBase{
   
    NetworkTable table = NetworkTableInstance.getDefault().getTable("limelight");
    NetworkTableEntry tx = table.getEntry("tx");
    NetworkTableEntry ty = table.getEntry("ty");
    double x;
    double y;
    double[] dis;

    @Override
    public void periodic() {
        x = tx.getDouble(0.0);
        y = ty.getDouble(0.0);
        dis = NetworkTableInstance.getDefault().getTable("limelight").getEntry("<targetpose_cameraspace>").getDoubleArray(new double[1]);

        SmartDashboard.putNumberArray("Distance", dis);
        SmartDashboard.putNumber("LimelightX", x);
        SmartDashboard.putNumber("LimelightY", y);
    }

    public double getVisionX()
    {
        return x;     
    }

    public double getVisionY()
    {
        return y;     
    }

}