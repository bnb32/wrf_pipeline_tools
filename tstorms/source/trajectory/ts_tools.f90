  module ts_tools_mod
  implicit none
  
  contains
 
!####################################################################
  
  SUBROUTINE TS_FILTER( work_dir )
  implicit none

  character(100) :: work_dir
!------------------------------------------------------------------------
! --- for land mask
!------------------------------------------------------------------------
  integer, parameter :: ix0 =   40                         
  integer, parameter :: iy0 = 1620 
  integer, parameter ::  ix = 360                         
  integer, parameter ::  iy = 180 
  real,    parameter ::  pi = 180.0  
  real,    parameter :: tpi = 360.0
  real,    parameter :: hpi =  90.0

  character*120 :: &
  landmask = '/glade/u/home/bbenton/RUNWORKFLOW/tstorms/source/trajectory/landsea.map'

  integer, dimension(ix0,iy0) :: mask0
  integer, dimension(ix, iy ) :: mask
  real                        :: dlon, lon0, dlat, lat0

  integer, dimension(2) :: shape2 = (/ ix, iy /)

!------------------------------------------------------------------------
! --- for latitude bounds
!------------------------------------------------------------------------
  real :: nlat =  40.0
  real :: slat = -40.0

!------------------------------------------------------------------------

  real        :: xcyc, ycyc, wind
  integer     :: year, month, day,  hour, ii, jj, max
  logical     :: keeper
  character*5 :: dummy

!========================================================================

 103 FORMAT( 2f8.2, 4i6 )
 104 FORMAT( a5,    5i6 )
 105 FORMAT( 3f8.2, 4i6 ) 
 200 format( 40i2 )

!------------------------------------------------------------------------
! --- set up land mask
!------------------------------------------------------------------------

   OPEN ( 10, FILE = trim(landmask) ) 
   do jj = 1,iy0
       read ( 10, 200 ) (mask0(ii,jj), ii=1,ix0)
   enddo    
   CLOSE( 10 )

   mask = RESHAPE( mask0, shape2 )
   mask = CSHIFT ( mask,  ix/2, 1 )

   lon0 =  0.0
   dlon =  tpi / FLOAT( ix )
   lat0 = -hpi + 0.5 *   pi / FLOAT( iy )                       
   dlat =       -2.0 * lat0 / FLOAT( iy - 1 )  

!------------------------------------------------------------------------
! --- process data
!------------------------------------------------------------------------

      OPEN( 12, file= TRIM(work_dir) // '/ori'       )
      OPEN( 14, file= TRIM(work_dir) // '/ori_filt'  )
      OPEN( 22, file= TRIM(work_dir) // '/traj'      )
      OPEN( 24, file= TRIM(work_dir) // '/traj_filt' )

!--- read a record
  100 READ( 12,103,end=101 ) xcyc, ycyc, year, month, day, hour

!--- filter by latitude
    keeper = ( ycyc <= nlat ) .and. ( ycyc >= slat ) 

!--- filter out storms over land
         jj = ( ycyc - lat0 ) / dlat + 1.5
         ii = ( xcyc - lon0 ) / dlon + 1.5
    if ( ii == 0  ) ii = ix
    if ( ii >  ix ) ii = ii - ix
    keeper = keeper .and. ( mask(ii,jj) == 0 ) 

!--- write a record
    if( keeper ) then
!   ====================================================
    WRITE( 14,103 ) xcyc, ycyc, year, month, day, hour
    READ ( 22,104 ) dummy, max, year, month, day, hour
    WRITE( 24,104 ) dummy, max, year, month, day, hour
    do ii = 1, max
    READ ( 22, 105 ) xcyc, ycyc, wind, year, month, day, hour
    WRITE( 24, 105 ) xcyc, ycyc, wind, year, month, day, hour
    end do
!   ====================================================
    else
!   ====================================================
    READ ( 22,104 ) dummy, max, year, month, day, hour
    do ii = 1, max
    READ ( 22, 105 ) xcyc, ycyc, wind
    end do
!   ====================================================
    endif

      go to 100
  101 continue
      CLOSE( 12 )
      CLOSE( 14 )
      CLOSE( 22 )
      CLOSE( 24 )

!========================================================================
  end SUBROUTINE TS_FILTER

!####################################################################
  
  SUBROUTINE TS_FILTER2( work_dir )
  implicit none

  character(100) :: work_dir
!------------------------------------------------------------------------
! --- for land mask
!------------------------------------------------------------------------
  integer, parameter :: ix0 =   40                         
  integer, parameter :: iy0 = 1620 
  integer, parameter ::  ix = 360                         
  integer, parameter ::  iy = 180 
  real,    parameter ::  pi = 180.0  
  real,    parameter :: tpi = 360.0
  real,    parameter :: hpi =  90.0

  character*120 :: &
  landmask = '/glade/u/home/bbenton/tstorms/RUNWORKFLOW/source/trajectory/landsea.map'
  integer, dimension(ix0,iy0) :: mask0
  integer, dimension(ix, iy ) :: mask
  real                        :: dlon, lon0, dlat, lat0

  integer, dimension(2) :: shape2 = (/ ix, iy /)

!------------------------------------------------------------------------
! --- for latitude bounds
!------------------------------------------------------------------------
  real :: nlat =  40.0
  real :: slat = -40.0

!------------------------------------------------------------------------

  real        :: xcyc, ycyc, wind, psl, vort
  integer     :: year, month, day,  hour, ii, jj, max
  logical     :: keeper
  character*5 :: dummy

!========================================================================

 103 FORMAT( 2f8.2, 4i6 )
 104 FORMAT( a5,    5i6 )
 105 FORMAT( 5f8.2, 4i6 ) 
 200 format( 40i2 )

!------------------------------------------------------------------------
! --- set up land mask
!------------------------------------------------------------------------

   OPEN ( 10, FILE = trim(landmask) ) 
   do jj = 1,iy0
       read ( 10, 200 ) (mask0(ii,jj), ii=1,ix0)
   enddo    
   CLOSE( 10 )

   mask = RESHAPE( mask0, shape2 )
   mask = CSHIFT ( mask,  ix/2, 1 )

   lon0 =  0.0
   dlon =  tpi / FLOAT( ix )
   lat0 = -hpi + 0.5 *   pi / FLOAT( iy )                       
   dlat =       -2.0 * lat0 / FLOAT( iy - 1 )  

!------------------------------------------------------------------------
! --- process data
!------------------------------------------------------------------------

      !OPEN( 12, file='ori'       )
      !OPEN( 14, file='ori_filt'  )
      !OPEN( 22, file='traj'      )
      !OPEN( 24, file='traj_filt' )

      OPEN( 12, file= TRIM(work_dir) // '/ori'       )
      OPEN( 14, file= TRIM(work_dir) // '/ori_filt'  )
      OPEN( 22, file= TRIM(work_dir) // '/traj'      )
      OPEN( 24, file= TRIM(work_dir) // '/traj_filt' )

!--- read a record
  100 READ( 12,103,end=101 ) xcyc, ycyc, year, month, day, hour

!--- filter by latitude
    keeper = ( ycyc <= nlat ) .and. ( ycyc >= slat ) 

!--- filter out storms over land
         jj = ( ycyc - lat0 ) / dlat + 1.5
         ii = ( xcyc - lon0 ) / dlon + 1.5
    if ( ii == 0  ) ii = ix
    if ( ii >  ix ) ii = ii - ix
    keeper = keeper .and. ( mask(ii,jj) == 0 ) 

!--- write a record
    if( keeper ) then
!   ====================================================
    WRITE( 14,103 ) xcyc, ycyc, year, month, day, hour
    READ ( 22,104 ) dummy, max, year, month, day, hour
    WRITE( 24,104 ) dummy, max, year, month, day, hour
    do ii = 1, max
    READ ( 22, 105 ) xcyc, ycyc, wind, psl, vort, year, month, day, hour
    WRITE( 24, 105 ) xcyc, ycyc, wind, psl, vort, year, month, day, hour
    end do
!   ====================================================
    else
!   ====================================================
    READ ( 22,104 ) dummy, max, year, month, day, hour
    do ii = 1, max
    READ ( 22, 105 ) xcyc, ycyc, wind, psl, vort, year, month, day, hour
    end do
!   ====================================================
    endif

      go to 100
  101 continue
      CLOSE( 12 )
      CLOSE( 14 )
      CLOSE( 22 )
      CLOSE( 24 )

!========================================================================
  end SUBROUTINE TS_FILTER2

!####################################################################
  
  SUBROUTINE TS_FILTER3( work_dir )
  implicit none

  character(100) :: work_dir
!------------------------------------------------------------------------
! --- for land mask
!------------------------------------------------------------------------
  integer, parameter :: ix0 =   40                         
  integer, parameter :: iy0 = 1620 
  integer, parameter ::  ix = 360                         
  integer, parameter ::  iy = 180 
  real,    parameter ::  pi = 180.0  
  real,    parameter :: tpi = 360.0
  real,    parameter :: hpi =  90.0

  character*120 :: &
  landmask = '/glade/u/home/bbenton/RUNWORKFLOW/tstorms/source/trajectory/landsea.map'

  integer, dimension(ix0,iy0) :: mask0
  integer, dimension(ix, iy ) :: mask
  real                        :: dlon, lon0, dlat, lat0

  integer, dimension(2) :: shape2 = (/ ix, iy /)

!------------------------------------------------------------------------
! --- for latitude bounds
!------------------------------------------------------------------------
  real :: nlat =  40.0
  real :: slat = -40.0

!------------------------------------------------------------------------

  real        :: xcyc, ycyc, wind, psl
  integer     :: year, month, day,  hour, ii, jj, max
  logical     :: keeper
  character*5 :: dummy

!========================================================================

 103 FORMAT( 2f8.2, 4i6 )
 104 FORMAT( a5,    5i6 )
 105 FORMAT( 4f8.2, 4i6 ) 
 200 format( 40i2 )

!------------------------------------------------------------------------
! --- set up land mask
!------------------------------------------------------------------------

   OPEN ( 10, FILE = trim(landmask) ) 
   do jj = 1,iy0
       read ( 10, 200 ) (mask0(ii,jj), ii=1,ix0)
   enddo    
   CLOSE( 10 )

   mask = RESHAPE( mask0, shape2 )
   mask = CSHIFT ( mask,  ix/2, 1 )

   lon0 =  0.0
   dlon =  tpi / FLOAT( ix )
   lat0 = -hpi + 0.5 *   pi / FLOAT( iy )                       
   dlat =       -2.0 * lat0 / FLOAT( iy - 1 )  

!------------------------------------------------------------------------
! --- process data
!------------------------------------------------------------------------

      OPEN( 12, file= TRIM(work_dir) // '/ori'       )
      OPEN( 14, file= TRIM(work_dir) // '/ori_filt'  )
      OPEN( 22, file= TRIM(work_dir) // '/traj'      )
      OPEN( 24, file= TRIM(work_dir) // '/traj_filt' )
      
      !OPEN( 12, file='ori'       )
      !OPEN( 14, file='ori_filt'  )
      !OPEN( 22, file='traj'      )
      !OPEN( 24, file='traj_filt' )

!--- read a record
  100 READ( 12,103,end=101 ) xcyc, ycyc, year, month, day, hour

!--- filter by latitude
    keeper = ( ycyc <= nlat ) .and. ( ycyc >= slat ) 

!--- filter out storms over land
         jj = ( ycyc - lat0 ) / dlat + 1.5
         ii = ( xcyc - lon0 ) / dlon + 1.5
    if ( ii == 0  ) ii = ix
    if ( ii >  ix ) ii = ii - ix
    keeper = keeper .and. ( mask(ii,jj) == 0 ) 

!--- write a record
    if( keeper ) then
!   ====================================================
    WRITE( 14,103 ) xcyc, ycyc, year, month, day, hour
    READ ( 22,104 ) dummy, max, year, month, day, hour
    WRITE( 24,104 ) dummy, max, year, month, day, hour
    do ii = 1, max
    READ ( 22, 105 ) xcyc, ycyc, wind, psl, year, month, day, hour
    WRITE( 24, 105 ) xcyc, ycyc, wind, psl, year, month, day, hour
    end do
!   ====================================================
    else
!   ====================================================
    READ ( 22,104 ) dummy, max, year, month, day, hour
    do ii = 1, max
    READ ( 22, 105 ) xcyc, ycyc, wind, psl, year, month, day, hour
    end do
!   ====================================================
    endif

      go to 100
  101 continue
      CLOSE( 12 )
      CLOSE( 14 )
      CLOSE( 22 )
      CLOSE( 24 )

!========================================================================
  end SUBROUTINE TS_FILTER3

!####################################################################

  SUBROUTINE TS_STATS ( do_filt, work_dir )
!===================================================================
!  use regions_mod
  implicit none

  character(100) :: work_dir


!-------------------------------------------------------------------

  logical, intent(in) :: do_filt

!-------------------------------------------------------------------
  integer, parameter :: ix  =  360                         
  integer, parameter :: iy  =  180 
  integer, parameter :: ireg = 12

  real,    parameter ::   pi = 180.0  
  real,    parameter ::  tpi = 360.0
  real,    parameter ::  hpi =  90.0

  real :: dlon, lon0, dlat, lat0

  integer, dimension(ix,iy) :: imask

  character*2, dimension(ireg) :: bx
  data bx /' G','WA','EA','WP','EP','NI','SI','AU','SP','SA','NH','SH'/

  character*120 :: &
  cmask = '/glade/u/home/bbenton/RUNWORKFLOW/tstorms/source/trajectory/imask_2'

!-------------------------------------------------------------------

  real     :: xcyc, ycyc,  div
  integer  :: year, month, day, hour
  integer  :: nr,   ny,    m,   indyr, indyr0
  integer  :: n, nc, ii, jj

  integer, dimension(13,ireg) :: icnt

  character*2, dimension(13) :: cmo = &
  (/ ' J',' F',' M',' A',' M',' J',' J',' A',' S',' O',' N',' D','Yr' /)

!===================================================================

!------------------------------------------------------------
! --- get mask
!------------------------------------------------------------

 open ( 10, FILE = trim(cmask), FORM = 'formatted' )
 do jj = 1,iy
    read(10,114) ( imask(ii,jj), ii=1,ix )
 end do
 close( 10 )
 114 format( 360i3  )

   lon0 =  0.0
   dlon =  tpi / FLOAT( ix )
   lat0 =  hpi - 0.5 *   pi / FLOAT( iy )                       
   dlat =        2.0 * lat0 / FLOAT( iy - 1 )  

!------------------------------------------------------------
! --- loop through file & count storms
!------------------------------------------------------------

  icnt(:,:) = 0

  if( do_filt) then
      OPEN( 12, file= TRIM(work_dir) // '/ori_filt' )
  else
      OPEN( 12, file= TRIM(work_dir) // '/ori' )
  endif

  100 continue
        READ( 12,*,end=101 ) xcyc, ycyc, year, month, day, hour

         jj = ( lat0 - ycyc ) / dlat + 1.5
         ii = ( xcyc - lon0 ) / dlon + 1.5
    if ( ii == 0  ) ii = ix
    if ( ii >  ix ) ii = ii - ix
         nr = imask(ii,jj)

                 icnt(month,1)  = icnt(month,1)  + 1
    if( nr > 0 ) icnt(month,nr) = icnt(month,nr) + 1

      go to 100
  101 continue
      CLOSE( 12 )

   icnt(1:12,ireg-1) = SUM( icnt(1:12,2:6 ), 2 )  ! NH
   icnt(1:12,ireg  ) = SUM( icnt(1:12,7:10), 2 )  ! SH

   icnt(13,1:ireg) = SUM( icnt(1:12,1:ireg), 1 )  ! year

!-----------------------------------------------------------
! --- output storm counts 
!------------------------------------------------------------

  OPEN( 12, file= TRIM(work_dir) // '/stats' )

  WRITE(12, *) '   '
  WRITE(12,*) 'NUMBER OF STORMS: ', icnt(13,1)
  WRITE(12, *) '   '
  WRITE(12,20) ( cmo(m), m = 1,13 )

  do nr = 1,ireg
  WRITE(12,21) bx(nr), ( icnt(m,nr), m = 1,13 )
  end do

  CLOSE(12)

  20 format( 2x, 2x, 13a6   )
  21 format( 2x, a2, 13i6   )

!===================================================================
  end SUBROUTINE TS_STATS

!####################################################################

 SUBROUTINE CJDAY( month, day, jday )
 implicit none

 integer, intent(in)    :: month, day
 integer, intent(out)   :: jday
 integer, dimension(12) :: ndays = (/ 31,28,31,30,31,30, &
                                      31,31,30,31,30,31 /)
                  jday = day
  if( month > 1 ) jday = jday + SUM( ndays(1:month-1) ) 

  end SUBROUTINE CJDAY

!####################################################################
  end module ts_tools_mod
