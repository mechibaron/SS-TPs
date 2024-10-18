package models;

import models.particles.Particle;
import models.particles.StaticParticle;
import models.particles.Velocity;
import models.walls.Wall;
import models.walls.WallType;

public class Event {

    public static void applyCollision(Particle p1, Obstacle obstacle) {
        if (obstacle instanceof StaticParticle sp)
            applyCollision(p1, sp);
        else if (obstacle instanceof Particle p2)
            applyCollision(p1, p2);
        else if (obstacle instanceof Wall w)
            applyCollision(p1, w.getType());
    }

    public static void applyCollision(Particle p1, Particle p2) {
        double deltaX = p1.getPosition().getX() - p2.getPosition().getX();
        double deltaY = p1.getPosition().getY() - p2.getPosition().getY();
        double sigma = p1.getRadius() + p2.getRadius();
        double deltaVX = p1.getVelocity().getX() - p2.getVelocity().getX();
        double deltaVY = p1.getVelocity().getY() - p2.getVelocity().getY();

        double deltas = deltaVX * deltaX + deltaVY * deltaY;
        double m1 = p1.getMass();
        double m2 = p2.getMass();

        double J = (2 * m1 * m2 * deltas) / (sigma * (m1 + m2));

        double Jx = (J * deltaX) / sigma;
        double Jy = (J * deltaY) / sigma;

        // Velocidades de la partícula actual (p2)
        p1.setVelocity(new Velocity(
                p1.getVelocity().getX() + Jx / m1,
                p1.getVelocity().getY() + Jy / m1));
        p2.setVelocity(new Velocity(
                p2.getVelocity().getX() - Jx / m2,
                p2.getVelocity().getY() - Jy / m2));
    }

    public static void applyCollision(Particle p1, StaticParticle p2) {
        double deltaX = p1.getPosition().getX() - p2.getPosition().getX();
        double deltaY = p1.getPosition().getY() - p2.getPosition().getY();
        double sigma = p1.getRadius() + p2.getRadius();
        double deltaVX = p1.getVelocity().getX() - p2.getVelocity().getX();
        double deltaVY = p1.getVelocity().getY() - p2.getVelocity().getY();

        double deltas = deltaVX * deltaX + deltaVY * deltaY;
        double m1 = p1.getMass();
        double m2 = p2.getMass();

        double J = (2 * m1 * m2 * deltas) / (sigma * (m1 + m2));

        double Jx = (J * deltaX) / sigma;
        double Jy = (J * deltaY) / sigma;

        p1.setVelocity(new Velocity(
                p1.getVelocity().getX() - Jx / m1,
                p1.getVelocity().getY() - Jy / m1
        ));
    }

    public static void applyCollision(Particle p1, WallType type) {
        Velocity newVelocity = switch (type) {
            case BOTTOM, TOP -> new Velocity(p1.getVelocity().getX(), -p1.getVelocity().getY());
            case RIGHT, LEFT -> new Velocity(-p1.getVelocity().getX(), p1.getVelocity().getY());
        };
        p1.setVelocity(newVelocity);
    }


}