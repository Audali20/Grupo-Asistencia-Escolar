DROP DATABASE Login;
CREATE DATABASE Login;
USE Login;

CREATE TABLE Registro_docentes (
Id INT AUTO_INCREMENT PRIMARY KEY,
Nombre VARCHAR(50),
Apellido VARCHAR(50),
Correo VARCHAR(50),
Contraseña VARCHAR(8)
);

CREATE TABLE Registro_estudiantes (
NIE INT PRIMARY KEY,
Nombre VARCHAR(50),
Apellido VARCHAR(50),
Correo VARCHAR(50),
Id_docente INT
);

CREATE TABLE Registro_asistencia (
NIE INT,
Nombre VARCHAR(50),
Apellido VARCHAR(50)
);

INSERT INTO registro_asistencia(NIE, Nombre, Apellido) SELECT DISTINCT(NIE), Nombre, Apellido FROM Registro_estudiantes;

ALTER TABLE Registro_estudiantes ADD CONSTRAINT fk_DoEst FOREIGN KEY (Id_docente) REFERENCES Registro_docentes(Id) ON DELETE CASCADE ON UPDATE CASCADE;


SELECT * FROM registro_docentes;
SELECT * FROM registro_estudiantes;
SELECT * FROM registro_asistencia;